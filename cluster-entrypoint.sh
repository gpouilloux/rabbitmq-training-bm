#!/bin/bash
set -e

# Start RMQ from entry point.
# This will ensure that environment variables passed
# will be honored
/usr/local/bin/docker-entrypoint.sh rabbitmq-server -detached

sleep 15s

rabbitmq-plugins enable rabbitmq_management rabbitmq_event_exchange rabbitmq_tracing rabbitmq_shovel rabbitmq_shovel_management

# Do the cluster dance
rabbitmqctl stop_app

# MUST have this line, otherwise the node will be blocked to join cluster again.
rabbitmqctl reset

rabbitmqctl join_cluster rabbit@rabbitmq1

# Stop the entire RMQ server. This is done so that we
# can attach to it again, but without the -detached flag
# making it run in the forground
rabbitmqctl stop

# Wait a while for the app to really stop
sleep 2s

# Start it
rabbitmq-server