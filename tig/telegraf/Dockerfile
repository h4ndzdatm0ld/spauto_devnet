FROM telegraf:latest

USER root

ADD telegraf.conf /telegraf.conf
COPY *.conf /etc/telegraf/telegraf.d/

RUN apt-get update && apt-get -y install build-essential

ADD run.sh /run.sh
ENTRYPOINT ["bash", "/run.sh"]
