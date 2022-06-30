from queue import channel

ack = True


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode())
    print(" [x] Properties %r" % properties)
    # time.sleep(body.count(b'.'))
    print(" [x] Done")
    if ack:
        ch.basic_ack(delivery_tag=method.delivery_tag)


queue_name = 'firehose'

channel.queue_declare(queue=queue_name, exclusive=False)

channel.queue_bind(exchange='amq.rabbitmq.trace',
                   queue=queue_name,
                   routing_key="#")

channel.basic_consume(queue=queue_name, on_message_callback=callback)

channel.start_consuming()
