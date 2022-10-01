"""Index service"""

import os
import json
import requests
from functools import partial

INDEX_SRV_ENDPOINT = os.environ["INDEX_SRV_ENDPOINT"]


def search(query, n, mode):
    if isinstance(query, list):
        query = json.dumps(query)
    payload = {"mode": mode, "query": query, "n": n}
    try:
        response = requests.get(f"{INDEX_SRV_ENDPOINT}/search", params=payload)
    except Exception as e:
        raise e
    if response.status_code != 200:
        raise Exception(response.text)
    return response.json().get("results")

vector_search = partial(search, mode="vector")
