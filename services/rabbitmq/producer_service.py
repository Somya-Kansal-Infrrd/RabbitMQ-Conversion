"""RabbitMQ producer service."""

import json

import pika

from configs.log import get_logger


QUEUE_NAME = "document_reconstruction"

logger = get_logger(__name__)


def publish_message(document_id: str) -> None:
    """Publish a document ID to RabbitMQ."""

    connection = pika.BlockingConnection(
        pika.ConnectionParameters("localhost", 5672)
    )

    channel = connection.channel()

    channel.queue_declare(
        queue=QUEUE_NAME,
        durable=True
    )

    message = {
        "documentId": document_id
    }

    channel.basic_publish(
        exchange="",
        routing_key=QUEUE_NAME,
        body=json.dumps(message)
    )

    logger.info("Sent document ID: %s", document_id)

    connection.close()

    logger.info("RabbitMQ connection closed")