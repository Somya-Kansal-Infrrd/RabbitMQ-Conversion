"""Services for reconstructing documents."""


def build_document(
    document_data: dict,
    fields: list[dict],
    pages: list[dict]
) -> dict:
    """Build a document in the original request format."""

    return {
        "id": document_data.get("_id", ""),
        "name": document_data.get("fileName", ""),
        "fileType": document_data.get("fileType", ""),
        "status": document_data.get("status", ""),
        "subStatus": document_data.get("subStatus", ""),
        "docType": document_data.get("docType", ""),
        "splitLevel": document_data.get("splitLevel", "0"),
        "alphaId": document_data.get("_id", ""),
        "fields": fields,
        "pages": pages,
        "documentExtractionStartDate":
            document_data.get("documentExtractionStartDate", ""),
        "documentReceivedDate":
            document_data.get("documentReceivedDate", ""),
        "lastModifiedDate":
            document_data.get("lastModifiedDate", ""),
        "sourceDocumentUrl":
            document_data.get("sourceDocumentUrl", ""),
        "isDocSigned":
            document_data.get("isDocSigned", False),
        "version":
            document_data.get("version", 1),
        "docSigned":
            document_data.get("docSigned", False),
        "totalPages":
            document_data.get("totalPages", 0)
    }
def build_request(
    document_data: dict,
    request_document: dict
) -> dict:
    """Build the original request body."""

    return {
        "requestId": document_data.get("requestId", ""),
        "status": document_data.get("status", ""),
        "documents": [request_document]
    }