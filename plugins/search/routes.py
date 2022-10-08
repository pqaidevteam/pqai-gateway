from functools import partial
import sys
from pathlib import Path
from pydantic import BaseModel
from fastapi import APIRouter

from plugins.search.obvious import Combiner

BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(BASE_DIR.as_posix())

from core.encoder_srv import encode
from core.index_srv import vector_search
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

vectorize = partial(encode, encoder="sbert")

class SearchRequest(BaseModel):
    query: str
    n: int = 10
    before: str = None
    after: str = None
    rerank: bool = False

def search(req: SearchRequest):
    qvec = vectorize(req.query)
    matches = vector_search(qvec, req.n)
    results = [SearchResult(*match) for match in matches]
    return {
        "query": req.query,
        "results": [r.json() for r in results]
    }

router = APIRouter()

@router.post('/search/102')
async def run_query(req: SearchRequest):
    return search(req)

@router.post("/search/103")
async def run_query_103(req: SearchRequest):
    results = search(req).get("results")
    docs = [r.get("abstract") for r in results]
    combiner = Combiner(req.query, docs)
    index_pairs = combiner.get_combinations(10)
    combinations = [[results[i], results[j]] for i, j in index_pairs]
    return {
        "query": req.query,
        "results": combinations
    }

@router.get('/patents/{pn}/claims/{claim_no}/prior-art')
async def find_prior_art(pn: str, claim_no: int):
    doc = Document(pn)
    query = doc.json().get("claims")[claim_no-1]
    before = doc.json().get("publication_date")
    req = SearchRequest(query=query, before=before, n=10)
    response = search(req)
    return response

@router.get('/patents/{pn}/similar')
async def find_similar(pn: str):
    doc = Document(pn)
    query = doc.json().get("abstract")
    req = SearchRequest(query=query, n=10)
    response = search(req)
    return response
