# Use uma imagem Python oficial
FROM python:3.9-slim

ENV CASSANDRA_CLUSTER_NAME=TestCluster \
    CASSANDRA_SEEDS=cassandra_node01,cassandra_node02,cassandra_node03 \
    CASSANDRA_ENDPOINT_SNITCH=GossipingPropertyFileSnitch \
    CASSANDRA_AUTHENTICATOR=PasswordAuthenticator \
    CASSANDRA_AUTHORIZER=CassandraAuthorizer

# Copie o script Python para dentro do contêiner
COPY cql/init_cassandra.py /etc/cassandra/init_cassandra.py
COPY credentials/cassandra.credentials /etc/cassandra/cassandra.credentials

# Defina as permissões corretas para os arquivos copiados
RUN chmod 755 /etc/cassandra/init_cassandra.py \
    && chmod 755 /etc/cassandra/cassandra.credentials

# Instale as dependências do script Python
RUN pip install cassandra-driver

# Defina o comando padrão para executar o script Python
CMD ["python", "/etc/cassandra/init_cassandra.py"]
