"""RabbitMQ consumer service."""

from typing import Any, Callable

import pika

from configs.log import get_logger

QUEUE_NAME = "document_reconstruction"

logger = get_logger(__name__)


def start_consumer(
    callback: Callable[..., Any]
) -> None:
    """Connect to RabbitMQ and start consuming messages."""

    connection = pika.BlockingConnection(
        pika.ConnectionParameters("localhost")
    )

    channel = connection.channel()

    channel.queue_declare(
        queue=QUEUE_NAME,
        durable=True
    )

    channel.basic_consume(
        queue=QUEUE_NAME,
        on_message_callback=callback
    )

    logger.info("Consumer started")
    logger.info("Waiting for messages...")

    channel.start_consuming()