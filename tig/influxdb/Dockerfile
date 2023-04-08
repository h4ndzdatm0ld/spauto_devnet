FROM influxdb:latest

USER root

ADD ./influxdb.template.conf /influxdb.template.conf

ADD run.sh /run.sh
ENTRYPOINT ["bash", "/run.sh"]
