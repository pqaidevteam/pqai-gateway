import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Response
from typing import Union, List, Optional
from pydantic import BaseModel

load_dotenv()

app=FastAPI()

class SearchRequest(BaseModel):
    query: str
    before: Optional[str]
    after: Optional[str]
    n: Optional[int, 10]
    rerank: bool


@app.post('/search')
async def run_query():
    pass

@app.get('/patents/{pn}/claims/{n}/prior-art')
async def find_prior_art(pn: str, n: int):
    pass

@app.get('/patents/{pn}/similar')
async def find_similar(pn: str):
    pass


if __name__ == "__main__":
    port = int(os.environ['PORT'])
    uvicorn.run(app, host="0.0.0.0", port=port)