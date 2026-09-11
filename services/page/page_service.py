"""Services for finding and converting pages."""


def find_pages(
    pages: list[dict],
    document_id: str
) -> list[dict]:
    """Find all pages belonging to a document."""

    document_pages = []

    for page in pages:
        if page.get("documentId") == document_id:
            document_pages.append(page)

    return document_pages


def build_pages(
    document_pages: list[dict]
) -> list[dict]:
    """Convert pages into request page format."""

    request_pages = []

    for page in document_pages:
        request_page = {
            "id": page.get("_id", ""),
            "pageNumber": page.get("pageNumber", 0),
            "status": page.get("status", ""),
            "dpiRes": page.get("dpiRes", ""),
            "rotation": page.get("rotation", "")
        }

        request_pages.append(request_page)

    return request_pages