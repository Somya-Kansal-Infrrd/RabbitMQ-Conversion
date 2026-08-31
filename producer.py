import json
import pika

# The document we want to reconstruct
DOCUMENT_ID = "d75a84af-cbe5-4d92-85b7-4558f533287b_document-1"


# Connect to RabbitMQ
connection = pika.BlockingConnection(
    pika.ConnectionParameters("localhost")
)

channel = connection.channel()


# Create a queue
channel.queue_declare(
    queue="document_reconstruction"
)


# Message that we want to send
message = {
    "documentId": DOCUMENT_ID
}


# Send message to RabbitMQ
channel.basic_publish(
    exchange="",
    routing_key="document_reconstruction",
    body=json.dumps(message)
)


print("Message sent successfully!")
print(json.dumps(message, indent=2))


# Close connection
connection.close()

print("RabbitMQ connection closed")