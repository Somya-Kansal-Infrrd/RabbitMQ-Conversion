import json
import pika


# --------------------------------
# Load JSON files
# --------------------------------

with open("document.json", "r") as file:
    documents = json.load(file)

with open("page.json", "r") as file:
    pages = json.load(file)

with open("extraction_field.json", "r") as file:
    extraction_fields = json.load(file)


print("JSON files loaded")
print("Total documents:", len(documents))
print("Total pages:", len(pages))
print("Total extraction fields:", len(extraction_fields))


# --------------------------------
# Connect to RabbitMQ
# --------------------------------

connection = pika.BlockingConnection(
    pika.ConnectionParameters("localhost")
)

channel = connection.channel()


# --------------------------------
# Create queue
# --------------------------------

channel.queue_declare(
    queue="document_reconstruction"
)


# --------------------------------
# Message processing function
# --------------------------------

def process_message(ch, method, properties, body):

    # Convert RabbitMQ message from JSON string to Python dictionary
    message = json.loads(body)

    document_id = message["documentId"]

    print("\nReceived document ID:")
    print(document_id)


    # --------------------------------
    # Find document
    # --------------------------------

    document_data = None

    for document in documents:

        if document.get("_id") == document_id:

            document_data = document
            break


    if document_data is None:

        print("Document not found")

        ch.basic_ack(
            delivery_tag=method.delivery_tag
        )

        return


    print("\nDocument found:")
    print(document_data["_id"])


    # --------------------------------
    # Find pages
    # --------------------------------

    document_pages = []

    for page in pages:

        if page.get("documentId") == document_id:

            document_pages.append(page)


    print(
        "Pages found:",
        len(document_pages)
    )


    # --------------------------------
    # Find extraction fields
    # --------------------------------

    document_fields = []

    for field in extraction_fields:

        if field.get("documentId") == document_id:

            document_fields.append(field)


    print(
        "Extraction fields found:",
        len(document_fields)
    )


    # --------------------------------
    # Build fields
    # --------------------------------

    fields = []

    for extraction in document_fields:

        field = {

            "name": extraction.get(
                "fieldName",
                ""
            ),

            "type": extraction.get(
                "fieldType",
                ""
            ),

            "dataType": extraction.get(
                "dataType",
                ""
            ),

            "confidence": extraction.get(
                "confidence",
                0
            ),

            "value": extraction.get(
                "value",
                ""
            ),

            "isCorrected": extraction.get(
                "isCorrected",
                False
            )
        }

        fields.append(field)


    # --------------------------------
    # Build pages
    # --------------------------------

    request_pages = []

    for page in document_pages:

        request_page = {

            "id": page.get(
                "_id",
                ""
            ),

            "pageNumber": page.get(
                "pageNumber",
                0
            ),

            "status": page.get(
                "status",
                ""
            ),

            "dpiRes": page.get(
                "dpiRes",
                ""
            ),

            "rotation": page.get(
                "rotation",
                ""
            )
        }

        request_pages.append(request_page)


    # --------------------------------
    # Build document
    # --------------------------------

    request_document = {

        "id": document_data.get(
            "_id",
            ""
        ),

        "name": document_data.get(
            "fileName",
            ""
        ),

        "fileType": document_data.get(
            "fileType",
            ""
        ),

        "status": document_data.get(
            "status",
            ""
        ),

        "subStatus": document_data.get(
            "subStatus",
            ""
        ),

        "docType": document_data.get(
            "docType",
            ""
        ),

        "splitLevel": document_data.get(
            "splitLevel",
            "0"
        ),

        "alphaId": document_data.get(
            "_id",
            ""
        ),

        "fields": fields,

        "pages": request_pages,

        "documentExtractionStartDate":
            document_data.get(
                "documentExtractionStartDate",
                ""
            ),

        "documentReceivedDate":
            document_data.get(
                "documentReceivedDate",
                ""
            ),

        "lastModifiedDate":
            document_data.get(
                "lastModifiedDate",
                ""
            ),

        "sourceDocumentUrl":
            document_data.get(
                "sourceDocumentUrl",
                ""
            ),

        "isDocSigned":
            document_data.get(
                "isDocSigned",
                False
            ),

        "version":
            document_data.get(
                "version",
                1
            ),

        "docSigned":
            document_data.get(
                "docSigned",
                False
            ),

        "totalPages":
            document_data.get(
                "totalPages",
                0
            )
    }


    # --------------------------------
    # Build original request
    # --------------------------------

    original_request = {

        "requestId":
            document_data.get(
                "requestId",
                ""
            ),

        "status":
            document_data.get(
                "status",
                ""
            ),

        "documents": [
            request_document
        ]
    }


    # --------------------------------
    # Print result
    # --------------------------------

    print("\nORIGINAL REQUEST BODY")

    print(
        json.dumps(
            original_request,
            indent=2,
            default=str
        )
    )


    # --------------------------------
    # Save result
    # --------------------------------

    with open(
        "reconstructed_request.json",
        "w"
    ) as file:

        json.dump(
            original_request,
            file,
            indent=2,
            default=str
        )


    print(
        "\nReconstructed request saved!"
    )


    # --------------------------------
    # Tell RabbitMQ message is done
    # --------------------------------

    ch.basic_ack(
        delivery_tag=method.delivery_tag
    )

    print(
        "Message processed successfully!"
    )


# --------------------------------
# Start consuming
# --------------------------------

channel.basic_consume(
    queue="document_reconstruction",
    on_message_callback=process_message
)


print("\nConsumer started")
print("Waiting for messages...")


channel.start_consuming()