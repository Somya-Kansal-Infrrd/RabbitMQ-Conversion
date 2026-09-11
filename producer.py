"""RabbitMQ document producer."""

from services.rabbitmq.producer_service import publish_message


document_ids = {
    "d75a84af-cbe5-4d92-85b7-4558f533287b_document-1",
    "7d8a614d-4dbc-47cb-b013-b38ed6e55ebf_document-1"
}


for document_id in document_ids:
    publish_message(document_id)