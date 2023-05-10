FROM influxdb:latest as influxdb

USER root

ADD ./influxdb.template.conf /etc/influxdb/influxdb.conf

RUN mkdir -p /var/log/influxdb/ && touch /var/log/influxdb/influxdb.log

# ADD run.sh /run.sh

# ENTRYPOINT ["bash", "/run.sh"]