"""Classes that wrap document data
"""

class Document:

    def __init__(self, data: dict):
        self._data = data

    def is_patent(self) -> bool:
        return "publicationNumber" in self._data

    @property
    def doc_id(self) -> str:
        key = "publicationNumber" if self.is_patent() else "id"
        return self._data[key]

    @property
    def publication_date(self) -> str:
        return self._data["publicationDate"]

    @property
    def title(self) -> str:
        return self._data["title"]

    @property
    def abstract(self) -> str:
        return self._data["abstract"]

    @property
    def claims(self) -> list:
        return self._data["claims"] if self.is_patent() else None

    def json(self) -> dict:
        return {
            "doc_id": self.doc_id,
            "title": self.title,
            "abstract": self.abstract,
            "publication_date": self.publication_date,
            "claims": self.claims
        }
            