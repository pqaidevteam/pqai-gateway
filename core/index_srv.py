"""Index service"""

import os
import json
from functools import partial, lru_cache
import requests

INDEX_SRV_ENDPOINT = os.environ["INDEX_SRV_ENDPOINT"]

@lru_cache(maxsize=1024)
def search(query, n, mode):
    if isinstance(query, list):
        query = json.dumps(query)
    payload = {"mode": mode, "query": query, "n": n}
    url = f"{INDEX_SRV_ENDPOINT}/search"
    try:
        response = requests.get(url, params=payload, timeout=5)
    except Exception as e:
        raise e
    if response.status_code != 200:
        raise Exception(response.text)
    return response.json().get("results")

vector_search = partial(search, mode="vector")
