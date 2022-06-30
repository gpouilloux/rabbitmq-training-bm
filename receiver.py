import logging

import pika
from pika.exchange_type import ExchangeType

LOGGER = logging.getLogger(__name__)


class Consumer(object):
    """A rabbitMQ consumer"""
    EXCHANGE = ''
    EXCHANGE_TYPE = ExchangeType.topic
    QUEUE = 'task_queue'
    ROUTING_KEY = '#'
    PREFETCH_COUNT = 1

    def __init__(self, amqp_url):
        self._channel = None
        self._connection = None
        self._url = amqp_url

    def connect(self):
        LOGGER.info('Connection to %s ...', self._url)
        return pika.SelectConnection(
                pika.ConnectionParameters(host='localhost'),
                on_open_callback=self.on_connection_open
        )

    def on_connection_open(self, _unused_connection):
        self._connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel):
        self._channel = channel
        self.start_consuming()

    def run(self):
        while True:
            try:
                self._connection = self.connect()
                self._connection.ioloop.start()
            except KeyboardInterrupt:
                self.close_connection()
                break

    def close_connection(self):
        if self._connection.is_closing or self._connection.is_closed:
            LOGGER.info('Connection closed, nothing to do here')
        else:
            self._connection.close()
            LOGGER.info('Connection closed')

    def start_consuming(self):
        self._channel.queue_declare(queue=self.QUEUE, durable=True)
        LOGGER.info('Start consuming')
        self._channel.basic_consume(
            self.QUEUE, self.on_message)

    def on_message(self, _channel, basic_deliver, _properties, body):
        LOGGER.info('Received message #%s: %s',
                    basic_deliver.delivery_tag, body)
        self._channel.basic_ack(basic_deliver.delivery_tag)


def main():
    logging.basicConfig(level=logging.INFO)
    amqp_url = 'amqp://guest:guest@localhost:5672/%2F'
    consumer = Consumer(amqp_url)
    consumer.run()


if __name__ == '__main__':
    main()
