#!/bin/bash
set -m
rabbitmq-server &
#rabbitmqctl await_startup
sleep 6
#rabbitmqctl add_user full_access test
#rabbitmqctl set_user_tags full_access "administrator"     #this makes the user a super user
#rabbitmqctl set_permissions -p "/" full_access ".*" ".*" ".*" # this too
rabbitmq-plugins enable rabbitmq_management rabbitmq_event_exchange rabbitmq_tracing rabbitmq_shovel rabbitmq_shovel_management
rabbitmqctl trace_on
fg %1
