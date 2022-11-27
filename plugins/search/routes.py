from functools import partial
import sys
import asyncio
from pathlib import Path
from pydantic import BaseModel
from fastapi import APIRouter

THIS_DIR = Path(__file__).resolve().parent
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(THIS_DIR.as_posix())
sys.path.append(BASE_DIR.as_posix())

from core.encoder_srv import encode
from core.index_srv import vector_search
from core.documents import Document
from core.db_srv import get_document

from filters import PublicationDateFilter
from obvious import Combiner


class SearchResult(Document):

    def __init__(self, data: dict, score: float):
        super().__init__(data)
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

async def search(req: SearchRequest):
    date_filter = PublicationDateFilter(req.after, req.before)
    qvec = vectorize(req.query)
    results = []
    limit = 200
    m = req.n
    if m > limit:
        raise Exception(f"Request result count exceeds limit = {limit}")
    while len(results) < req.n and m <= limit:
        neighbors = vector_search(qvec, m)
        doc_ids = [neighbor[0] for neighbor in neighbors]
        scores = [neighbor[1] for neighbor in neighbors]
        documents = await asyncio.gather(*map(get_document, doc_ids))
        results = [SearchResult(documents[i], scores[i]) for i in range(len(documents))]
        results = date_filter.apply(results)
        results = [r.json() for r in results]
        m = m * 2
    return {
        "query": req.query,
        "results": results
    }

router = APIRouter()

@router.post('/search/102')
async def run_query(req: SearchRequest):
    return await search(req)

@router.post("/search/103")
async def run_query_103(req: SearchRequest):
    results = (await search(req)).get("results")
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
    patent_data = await get_document(pn)
    doc = Document(patent_data)
    query = doc.json().get("claims")[claim_no-1]
    before = doc.json().get("publication_date")
    req = SearchRequest(query=query, before=before, n=10)
    response = await search(req)
    return response

@router.get('/patents/{pn}/similar')
async def find_similar(pn: str):
    patent_data = await get_document(pn)
    doc = Document(patent_data)
    query = doc.json().get("abstract")
    req = SearchRequest(query=query, n=10)
    response = await search(req)
    return response
