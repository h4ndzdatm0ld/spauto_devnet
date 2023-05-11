#!/bin/bash

set -m
CONFIG_FILE="/etc/telegraf/telegraf.conf"

echo "=> Starting Telegraf ..."
exec telegraf -config $CONFIG_FILE --config-directory /etc/telegraf/telegraf.d
