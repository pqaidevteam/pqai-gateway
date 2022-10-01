from core.documents import Document

class SearchResult(Document):

    def __init__(self, doc_id: str, score: float):
        super().__init__(doc_id)
        self.score = score
    
    def __repr__(self) -> str:
        return f"SearchResult({self.doc_id}, {self.score})"
    
    def __str__(self) -> str:
        return f"SearchResult({self.doc_id}, {self.score})"
    
    def json(self) -> dict:
        doc = super().json()
        doc.pop("claims")
        doc["score"] = self.score
        return doc
