import logging
import time
import configparser
from cassandra.cluster import Cluster, DCAwareRoundRobinPolicy, ExecutionProfile, EXEC_PROFILE_DEFAULT
from cassandra.auth import PlainTextAuthProvider

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

credentials_path = "/etc/cassandra/cassandra.credentials"

def load_credentials(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    username = config.get('authentication', 'username')
    password = config.get('authentication', 'password')
    return username, password

def connect_to_cassandra(username, password):
    # Configurações de autenticação
    auth_provider = PlainTextAuthProvider(username=username, password=password)

    # Criação do perfil de execução com especificação do datacenter local
    execution_profile = ExecutionProfile(load_balancing_policy=DCAwareRoundRobinPolicy(local_dc='dc1'))

    # Conexão com o cluster Cassandra
    cluster = Cluster(
        ['cassandra_node01', 'cassandra_node02', 'cassandra_node03'],
        auth_provider=auth_provider,
        protocol_version=5,
        execution_profiles={EXEC_PROFILE_DEFAULT: execution_profile}
    )

    # Conecta-se a uma sessão
    try:
        session = cluster.connect()
        return session
    except Exception as e:
        logger.error(f"Erro ao conectar ao Cassandra: {e}")
        raise

def create_keyspace_and_table(session):
    # Criação do keyspace e da tabela se não existirem
    session.execute("""
    CREATE KEYSPACE IF NOT EXISTS ycsb_keypace_node
    WITH REPLICATION = {'class': 'NetworkTopologyStrategy', 'replication_factor': 3}
    """)
    
    session.execute("USE ycsb_keypace_node")
    
    session.execute("""
    CREATE TABLE IF NOT EXISTS usertable (
        y_id varchar PRIMARY KEY,
        field0 varchar,
        field1 varchar,
        field2 varchar,
        field3 varchar,
        field4 varchar,
        field5 varchar,
        field6 varchar,
        field7 varchar,
        field8 varchar,
        field9 varchar
    )
    """)

def create_users_and_grant_permissions(session):
    # Cria usuários se não existirem
    session.execute("CREATE ROLE IF NOT EXISTS admin WITH PASSWORD = 'cassandra' AND SUPERUSER = true AND LOGIN = true")
    session.execute("CREATE ROLE IF NOT EXISTS appuser WITH PASSWORD = 'cassandra' AND LOGIN = true")
    
    # Verifica se o keyspace existe antes de conceder permissões
    if 'ycsb_keypace_node' not in session.cluster.metadata.keyspaces:
        logger.error("Keyspace 'ycsb_keypace_node' não foi criado corretamente.")
        return
    
    # Concede permissões específicas para appuser no keyspace criado
    try:
        session.execute("GRANT SELECT ON KEYSPACE ycsb_keypace_node TO appuser")
        session.execute("GRANT MODIFY ON KEYSPACE ycsb_keypace_node TO appuser")
    except Exception as e:
        logger.error(f"Erro ao conceder permissões: {e}")

    # Concede permissões gerais de leitura em todos os keyspaces
    try:
        session.execute("GRANT SELECT ON ALL KEYSPACES TO appuser")
    except Exception as e:
        logger.error(f"Erro ao conceder permissões gerais: {e}")

def main():
    # Carregar credenciais do arquivo
    username, password = load_credentials(credentials_path)

    # Conectar-se ao cluster Cassandra
    time.sleep(25)  # Aumentar o tempo de espera
    session = connect_to_cassandra(username, password)

    # Criar o keyspace e a tabela
    create_keyspace_and_table(session)

    # Criar usuários e conceder permissões
    create_users_and_grant_permissions(session)

if __name__ == "__main__":
    main()
