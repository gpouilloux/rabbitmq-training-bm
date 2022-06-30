import sys
import pika
from pika.exceptions import ChannelClosedByBroker, UnroutableError

from queue import channel

message = ' '.join(sys.argv[1:]) or "Hello World!"

try:
    message_must_be_routable = True
    channel.confirm_delivery()

    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.TRANSIENT_DELIVERY_MODE
        ),
        mandatory=message_must_be_routable
    )

    print(" [x] Sent %r" % message)

except (ChannelClosedByBroker, UnroutableError) as e:
    print("Message not routable")
else:
    print("Message routed ✅")
