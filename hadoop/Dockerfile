#FROM bde2020/hadoop-base:2.0.0-hadoop2.7.4-java8
#FROM openjdk:8-jdk-slim
FROM eclipse-temurin:8-jdk-focal

WORKDIR /app

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install requests

ENV HADOOP_VERSION=2.7.4
ENV HADOOP_HOME=/opt/hadoop
ENV PATH=$PATH:$HADOOP_HOME/bin

RUN curl -sL https://archive.apache.org/dist/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz | tar -xz -C /opt/ \
    && mv /opt/hadoop-$HADOOP_VERSION $HADOOP_HOME

WORKDIR /app

COPY mapper.py reducer.py run_job.sh ./

RUN sed -i 's/±r$//' run_job.sh && \
    chmod +x mapper.py reducer.py run_job.sh

CMD ["./run_job.sh"]