from core.db_srv import get_document

class Document:

    def __init__(self, doc_id: str):
        self.doc_id = doc_id
        self._data = get_document(doc_id)

    def json(self) -> dict:
        return {
            "doc_id": self.doc_id,
            "title": self._data["title"],
            "abstract": self._data["abstract"],
            "publication_date": self._data["publicationDate"],
            "claims": self._data["claims"]
        }
