"""RabbitMQ consumer for document reconstruction."""

import json
import sys
from services.data.data_service import load_json_file
from services.document.document_service import find_document
from services.field.field_service import find_fields, build_fields
from services.output.output_service import save_output
from services.page.page_service import find_pages, build_pages
from configs.log import get_logger
from services.rabbitmq.consumer_service import start_consumer
from services.reconstruction.reconstruction_service import (
    build_document,
    build_request
)


consumer_name = sys.argv[1] if len(sys.argv) > 1 else "Consumer"

logger = get_logger(__name__)


# Load JSON files

documents = load_json_file("document.json")
pages = load_json_file("page.json")
extraction_fields = load_json_file("extraction_field.json")

logger.info("JSON files loaded")
logger.info("Total documents: %s", len(documents))
logger.info("Total pages: %s", len(pages))
logger.info("Total extraction fields: %s", len(extraction_fields))


def process_message(
    ch,
    method,
    properties,
    body: bytes
) -> None:
    """Process a document reconstruction message."""

    logger.info("%s received a message", consumer_name)

    # Convert RabbitMQ message to Python dictionary
    message = json.loads(body)

    document_id = message["documentId"]

    logger.info("Received document ID: %s", document_id)

    # Find document
    document_data = find_document(
        documents,
        document_id
    )

    if document_data is None:
        logger.warning("Document not found")

        ch.basic_ack(
            delivery_tag=method.delivery_tag
        )

        return

    logger.info("Document found: %s", document_data["_id"])

    # Find pages
    document_pages = find_pages(
        pages,
        document_id
    )

    logger.info("Pages found: %s", len(document_pages))

    # Find extraction fields
    document_fields = find_fields(
        extraction_fields,
        document_id
    )

    logger.info(
    "Extraction fields found: %s",
    len(document_fields)
)

    # Build fields
    fields = build_fields(
        document_fields
    )

    # Build pages
    request_pages = build_pages(
        document_pages
    )

    # Build document
    request_document = build_document(
        document_data,
        fields,
        request_pages
    )

    # Build original request
    original_request = build_request(
        document_data,
        request_document
    )

    # Print result
    logger.info("ORIGINAL REQUEST BODY")

    print(
        json.dumps(
            original_request,
            indent=2,
            default=str
        )
    )

    # Save result
    output_file = save_output(
        document_id,
        original_request
    )

    logger.info(
    "Reconstructed request saved to %s",
    output_file
)

    # Tell RabbitMQ message is done
    ch.basic_ack(
        delivery_tag=method.delivery_tag
    )

    logger.info("Message processed successfully!")


# Start consuming
start_consumer(process_message)