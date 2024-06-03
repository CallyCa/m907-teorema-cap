# Base image
FROM cassandra:latest

ARG VERSION=0.18.0

# Install curl and Python for cqlsh
RUN apt-get update && apt-get install -y curl python3 python3-pip iproute2 && \
    pip3 install cqlsh cassandra-driver docker && \
    rm -rf /var/lib/apt/lists/*

# Ensure the /app directory exists without trying to create it if it already exists
RUN mkdir -p /app &&\
    curl -O --location https://github.com/CallyCa/ycsb-python3/releases/download/v${VERSION}/ycsb-${VERSION}.tar.gz && \
    tar xfvz ycsb-${VERSION}.tar.gz -C /app &&\
    rm ycsb-${VERSION}.tar.gz

WORKDIR /app/ycsb-${VERSION}

# Add JDBC driver for Cassandra
RUN mkdir -p lib && \
    curl -O --location https://repo1.maven.org/maven2/com/datastax/oss/java-driver-core/4.9.0/java-driver-core-4.9.0.jar --output lib/

# Copy the network_failures script
COPY script/convert_to_json.py /app/ycsb-${VERSION}/script/convert_to_json.py
COPY script/network_failures.py /app/ycsb-${VERSION}/script/network_failures.py
COPY results/ /app/ycsb-${VERSION}/results

COPY entrypoint.sh ./bin/

ENTRYPOINT ["/app/ycsb-0.18.0/bin/entrypoint.sh"]

# Optionally, if you want to run the network_failures.py script as the default command
CMD ["python3", "/app/ycsb-${VERSION}/script/network_failures.py"]