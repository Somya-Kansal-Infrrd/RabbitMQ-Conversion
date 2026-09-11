"""Services for finding document information."""


def find_document(
    documents: list[dict],
    document_id: str
) -> dict | None:
    """Find a document using its document ID."""

    for document in documents:
        if document.get("_id") == document_id:
            return document

    return None