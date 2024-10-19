# Use a base image with Java installed
FROM openjdk:11-jre-slim

# Set environment variables
ENV KAFKA_VERSION=3.4.0
ENV SCALA_VERSION=2.13
ENV PROTOBUF_VERSION=3.21.12

# Install necessary tools
RUN apt-get update && apt-get install -y wget curl

# Download and install Kafka
RUN wget https://downloads.apache.org/kafka/${KAFKA_VERSION}/kafka_${SCALA_VERSION}-${KAFKA_VERSION}.tgz \
    && tar -xzf kafka_${SCALA_VERSION}-${KAFKA_VERSION}.tgz \
    && mv kafka_${SCALA_VERSION}-${KAFKA_VERSION} /kafka \
    && rm kafka_${SCALA_VERSION}-${KAFKA_VERSION}.tgz

# Download and install Protobuf
RUN wget https://github.com/protocolbuffers/protobuf/releases/download/v${PROTOBUF_VERSION}/protoc-${PROTOBUF_VERSION}-linux-x86_64.zip \
    && unzip protoc-${PROTOBUF_VERSION}-linux-x86_64.zip -d /usr/local \
    && rm protoc-${PROTOBUF_VERSION}-linux-x86_64.zip

# Set up Kafka configuration for KRaft (no ZooKeeper)
RUN mkdir -p /kafka/kraft-config
COPY server.properties /kafka/kraft-config/server.properties

# Generate a cluster ID
RUN /kafka/bin/kafka-storage.sh random-uuid > /kafka/kraft-config/cluster-id

# Set up the volume for Kafka data
VOLUME /kafka/kraft-data

# Expose Kafka port
EXPOSE 9092

# Start Kafka
CMD ["/bin/sh", "-c", "/kafka/bin/kafka-storage.sh format -t $(cat /kafka/kraft-config/cluster-id) -c /kafka/kraft-config/server.properties && /kafka/bin/kafka-server-start.sh /kafka/kraft-config/server.properties"]