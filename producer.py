import json
import pika

document_ids = {
    "d75a84af-cbe5-4d92-85b7-4558f533287b_document-1",
    "7d8a614d-4dbc-47cb-b013-b38ed6e55ebf_document-1"
}

connection = pika.BlockingConnection(
    pika.ConnectionParameters("localhost", 5672)
)

channel = connection.channel()

channel.queue_declare(
    queue="document_reconstruction",
    durable=True
)

for document_id in document_ids:

    message = {
        "documentId": document_id
    }

    channel.basic_publish(
        exchange="",
        routing_key="document_reconstruction",
        body=json.dumps(message)
    )

    print("Sent:", document_id)

connection.close()

print("RabbitMQ connection closed")