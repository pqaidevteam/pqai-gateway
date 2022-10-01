import os
from functools import partial
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

load_dotenv()

from core.encoder_srv import encode
from core.index_srv import vector_search
from core.search import SearchResult
from core.documents import Document

vectorize = partial(encode, encoder="sbert")

app=FastAPI()

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
    # TODO: Account for filters and handle rerank condition
    return {
        "query": req.query,
        "results": [r.json() for r in results]
    }

@app.post('/search')
async def run_query(req: SearchRequest):
    return search(req)


@app.get('/patents/{pn}/claims/{claim_no}/prior-art')
async def find_prior_art(pn: str, claim_no: int):
    doc = Document(pn)
    query = doc.json().get("claims")[claim_no-1]
    before = doc.json().get("publication_date")
    req = SearchRequest(query=query, before=before, n=10)
    return search(req)

@app.get('/patents/{pn}/similar')
async def find_similar(pn: str):
    doc = Document(pn)
    query = doc.json().get("abstract")
    req = SearchRequest(query=query, n=10)
    response = search(req)
    return response


if __name__ == "__main__":
    port = int(os.environ['PORT'])
    uvicorn.run(app, host="0.0.0.0", port=port)
