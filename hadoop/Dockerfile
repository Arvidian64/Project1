FROM bde2020/hadoop-base:2.0.0-hadoop2.7.4-java8

WORKDIR /app

RUN apt-get update && apt-get install -y python3 python3-pip curl && \
    pip3 install requests

COPY mapper.py reducer.py run_job.sh ./

RUN chmod +x mapper.py reducer.py run_job.sh

CMD ["./run_job.sh"]