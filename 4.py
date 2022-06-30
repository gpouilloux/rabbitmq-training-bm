import sys
import pika
from pika.exceptions import ChannelClosedByBroker, UnroutableError

from queue import channel

message = ' '.join(sys.argv[1:]) or "Hello World!"

channel.basic_publish(
    exchange='',
    routing_key='my-quorum-q',
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=pika.spec.TRANSIENT_DELIVERY_MODE
    ),
)

print(" [x] Sent %r" % message)

