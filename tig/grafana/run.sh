#!/bin/bash -e
# : "${GF_PATHS_DATA:=/var/lib/grafana}"
# : "${GF_PATHS_LOGS:=/var/log/grafana}"
# : "${GF_PATHS_PLUGINS:=/var/lib/grafana/plugins}"
# : "${GF_PATHS_PROVISIONING:=/etc/grafana/provisioning}"

# chown -R grafana:grafana "$GF_PATHS_DATA" "$GF_PATHS_LOGS"
# chown -R grafana:grafana /etc/grafana

###############################################################
# Creating Default Data Source

# # Set new Data Source name
# INFLUXDB_DATA_SOURCE="InfluxDB"
# INFLUXDB_DATA_SOURCE_WEB="$INFLUXDB_DATA_SOURCE"
# echo "The INFLUXDB Data Source Web is: $INFLUXDB_DATA_SOURCE_WEB"
# # Set information about grafana host
# GRAFANA_URL=`hostname -i`

# # Check $INFLUXDB_DATA_SOURCE status
# INFLUXDB_DATA_SOURCE_STATUS=`curl -s -L -i \
#  -H "Accept: application/json" \
#  -H "Content-Type: application/json" \
#  -X GET http://${GRAFANA_USER}:${GRAFANA_PASSWORD}@${GRAFANA_URL}:${GRAFANA_PORT}/api/datasources/name/${INFLUXDB_DATA_SOURCE_WEB} | head -1 | awk '{print $2}'`

# echo "THE INFUXDB DATA SOURCE STATUS IS: "
# echo "$INFLUXDB_DATA_SOURCE_STATUS"
# #Debug Time!
# curl -s -L -i \
#  -H "Accept: application/json" \
#  -H "Content-Type: application/json" \
#  -X GET http://${GRAFANA_USER}:${GRAFANA_PASSWORD}@${GRAFANA_URL}:${GRAFANA_PORT}/api/datasources/name/${INFLUXDB_DATA_SOURCE_WEB} >>$GF_PATHS_LOGS/grafana.log 2>>$GF_PATHS_LOGS/grafana.log 
# echo "http://${GRAFANA_USER}:${GRAFANA_PASSWORD}@${GRAFANA_URL}:${GRAFANA_PORT}/api/datasources/name/${INFLUXDB_DATA_SOURCE_WEB}" >> $GF_PATHS_LOGS/grafana.log
# echo "INFLUXDB_DATA_SOURCE_STATUS: "$INFLUXDB_DATA_SOURCE_STATUS >> $GF_PATHS_LOGS/grafana.log
# echo "GRAFANA_URL: "$GRAFANA_URL >> $GF_PATHS_LOGS/grafana.log
# echo "GRAFANA_PORT: "$GRAFANA_PORT >> $GF_PATHS_LOGS/grafana.log
# echo "GRAFANA_USER: "$GRAFANA_USER >> $GF_PATHS_LOGS/grafana.log
# echo "GRAFANA_PASSWORD: "$GRAFANA_PASSWORD >> $GF_PATHS_LOGS/grafana.log

# # Check if $INFLUXDB_DATA_SOURCE exists
# if [ ${INFLUXDB_DATA_SOURCE_STATUS} != 200 ]
# then
#   # If not exists, create one 
#   echo "Data Source: '"${INFLUXDB_DATA_SOURCE}"' not found in Grafana configuration"
#   echo "Creating Data Source: '"$INFLUXDB_DATA_SOURCE"'"
#   curl -L -i \
#    -H "Accept: application/json" \
#    -H "Content-Type: application/json" \
#    -X POST -d '{
#     "name":"'"${INFLUXDB_DATA_SOURCE}"'",
#     "type":"influxdb",
#     "url":"http://'"${INFLUXDB_HOST}"':'"${INFLUXDB_PORT}"'",
#     "access":"proxy",
#     "basicAuth":false,
#     "database": "'"${INFLUXDB_DATABASE}"'",
#     "user":"'"${INFLUXDB_ADMIN_USER}"'",
#     "password":"'"${INFLUXDB_ADMIN_PASSWORD}"'"}
#   ' \
#   http://${GRAFANA_USER}:${GRAFANA_PASSWORD}@${GRAFANA_URL}:${GRAFANA_PORT}/api/datasources
# else
#   #Continue if it doesn't exists
#   echo "Data Source '"${INFLUXDB_DATA_SOURCE}"' already exists."
# fi

# tail -f $GF_PATHS_LOGS/grafana.log
