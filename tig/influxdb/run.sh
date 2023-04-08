#!/bin/bash

set -m
# Protects script from continuing with an error
set -eu -o pipefail
# Ensures environment variables are set
export INFLUXDB_MODE=$INFLUXDB_MODE
export INFLUXDB_USERNAME=$INFLUXDB_USERNAME
export INFLUXDB_PASSWORD=$INFLUXDB_PASSWORD
export INFLUXDB_ORG=$INFLUXDB_ORG
export INFLUXDB_BUCKET=$INFLUXDB_BUCKET
export INFLUXDB_RETENTION=$INFLUXDB_RETENTION
export INFLUXDB_ADMIN_TOKEN=$INFLUXDB_ADMIN_TOKEN
export INFLUXDB_PORT=$INFLUXDB_PORT
export INFLUXDB_HOST=$INFLUXDB_HOST

CONFIG_TEMPLATE="/influxdb.template.conf"
CONFIG_FILE="/etc/influxdb/influxdb.conf"
CURR_TIMESTAMP=`date +%s`

mv -v $CONFIG_FILE $CONFIG_FILE.$CURR_TIMESTAMP
cp -v $CONFIG_TEMPLATE $CONFIG_FILE

exec influxd -config=$CONFIG_FILE 1>>/var/log/influxdb/influxdb.log 2>&1 &
sleep 5

USER_EXISTS=`influx -host=localhost -port=${INFLUXDB_PORT} -execute="SHOW USERS" | awk '{print $1}' | grep "${INFLUXDB_ADMIN_USER}" | wc -l`

if [ -n ${USER_EXISTS} ]
then
  influx -host=localhost -port=${INFLUXDB_PORT} -execute="CREATE USER ${INFLUXDB_ADMIN_USER} WITH PASSWORD '${INFLUXDB_ADMIN_PASSWORD}' WITH ALL PRIVILEGES"
  influx -host=localhost -port=${INFLUXDB_PORT} -username=${INFLUXDB_ADMIN_USER} -password="${INFLUXDB_ADMIN_PASSWORD}" -execute="create database ${INFLUXDB_DATABASE}"
  influx -host=localhost -port=${INFLUXDB_PORT} -username=${INFLUXDB_ADMIN_USER} -password="${INFLUXDB_ADMIN_PASSWORD}" -execute="grant all PRIVILEGES on ${INFLUXDB_DATABASE} to ${INFLUXDB_ADMIN_USER}"
fi 

# Conducts initial InfluxDB using the CLI
influx setup --skip-verify --bucket ${INFLUXDB_BUCKET} --retention ${INFLUXDB_RETENTION} --token ${INFLUXDB_ADMIN_TOKEN} --org ${INFLUXDB_ORG} --username ${INFLUXDB_USERNAME} --password ${INFLUXDB_PASSWORD} --host http://${INFLUXDB_HOST}:8086 --force


tail -f /var/log/influxdb/influxdb.log
