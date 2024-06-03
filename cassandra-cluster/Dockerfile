# Especifica a imagem base do Cassandra
FROM cassandra:latest

# Define variáveis de ambiente para a configuração do Cassandra
ENV CASSANDRA_CLUSTER_NAME=TestCluster \
    CASSANDRA_SEEDS=cassandra_node01,cassandra_node02,cassandra_node03 \
    CASSANDRA_ENDPOINT_SNITCH=GossipingPropertyFileSnitch \
    CASSANDRA_AUTHENTICATOR=PasswordAuthenticator \
    CASSANDRA_AUTHORIZER=CassandraAuthorizer

# Copia os arquivos de configuração e scripts necessários para o contêiner
COPY ./common/cql/init_cassandra.py /etc/cassandra/init_cassandra.py
COPY ./common/credentials/cassandra.credentials /etc/cassandra/cassandra.credentials
COPY ./node01/conf/cassandra.yaml /etc/cassandra/cassandra.yaml
COPY ./node01/conf/init-script.sh /etc/cassandra/init-script.sh
COPY ./node01/conf/env/cassandra-env.sh /etc/cassandra/cassandra-env.sh

# Define permissões adequadas para os arquivos de configuração e scripts
RUN chmod 755 /etc/cassandra/init_cassandra.py \
    && chmod 755 /etc/cassandra/cassandra.credentials \
    && chmod 755 /etc/cassandra/cassandra.yaml \
    && chmod 755 /etc/cassandra/init-script.sh \
    && chmod 755 /etc/cassandra/cassandra-env.sh

# Exponha as portas necessárias para o Cassandra
EXPOSE 9042 7199

# Comando para iniciar o Cassandra
CMD ["cassandra", "-f"]