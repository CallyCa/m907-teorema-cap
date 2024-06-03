# Base image
FROM mongo:5.0

ARG VERSION=0.18.0

# Install necessary tools, Java, and Python packages
RUN apt-get update && apt-get install -y curl python3 python3-pip iproute2 openjdk-11-jre-headless && \
    pip3 install pymongo docker && \
    rm -rf /var/lib/apt/lists/*

# Ensure the /app directory exists and download YCSB
RUN mkdir -p /app && \
    curl -O --location https://github.com/CallyCa/ycsb-python3/releases/download/v${VERSION}/ycsb-${VERSION}.tar.gz && \
    tar xfvz ycsb-${VERSION}.tar.gz -C /app && \
    rm ycsb-${VERSION}.tar.gz

WORKDIR /app/ycsb-${VERSION}

# Copy the network_failures script
COPY scripts/convert_to_json.py /app/ycsb-${VERSION}/script/convert_to_json.py
COPY scripts/network_failures.py /app/ycsb-${VERSION}/scripts/network_failures.py
COPY results/ /app/ycsb-${VERSION}/results

# Copy the entrypoint script and set executable permissions
COPY entrypoint.sh ./bin/
RUN chmod +x ./bin/entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/app/ycsb-0.18.0/bin/entrypoint.sh"]

# Optionally, if you want to run the network_failures.py script as the default command
CMD ["python3", "/app/ycsb-0.18.0/scripts/network_failures.py"]