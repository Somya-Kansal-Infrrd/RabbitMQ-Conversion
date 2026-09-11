"""Services for finding and converting extraction fields."""


def find_fields(
    extraction_fields: list[dict],
    document_id: str
) -> list[dict]:
    """Find all extraction fields belonging to a document."""

    document_fields = []

    for field in extraction_fields:
        if field.get("documentId") == document_id:
            document_fields.append(field)

    return document_fields


def build_fields(
    document_fields: list[dict]
) -> list[dict]:
    """Convert extraction fields into request field format."""

    fields = []

    for extraction in document_fields:
        field = {
            "name": extraction.get("fieldName", ""),
            "type": extraction.get("fieldType", ""),
            "dataType": extraction.get("dataType", ""),
            "confidence": extraction.get("confidence", 0),
            "value": extraction.get("value", ""),
            "isCorrected": extraction.get("isCorrected", False)
        }

        fields.append(field)

    return fields