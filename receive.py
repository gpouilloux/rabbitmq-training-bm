from queue import channel

ack = True


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode())
    # time.sleep(body.count(b'.'))
    print(" [x] Done")
    if ack:
        ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue='task_queue', on_message_callback=callback)

channel.start_consuming()
