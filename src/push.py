import os
import pika
from pika import DeliveryMode


def publish(data):
    mq_url = os.getenv("MQ_URL")
    parameters = pika.URLParameters(mq_url)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.basic_publish(
        "v2tool",
        "standard_key",
        data,
        pika.BasicProperties(
            content_type="text/plain", delivery_mode=DeliveryMode.Transient
        ),
    )
    connection.close()
