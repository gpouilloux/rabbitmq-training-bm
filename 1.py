import sys
from queue import channel

message = ' '.join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(
    exchange='',
    routing_key='task_queue',
    body=message
)

print(" [x] Sent %r" % message)
