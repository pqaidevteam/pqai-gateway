"""Database service
"""

import os
from functools import lru_cache
import requests

DB_SRV_ENDPOINT = os.environ["DB_SRV_ENDPOINT"]

@lru_cache(maxsize=1024)
def get_document(doc_id: str) -> dict:
    """Get document by id"""
    url = f"{DB_SRV_ENDPOINT}/patents/{doc_id}"
    try:
        response = requests.get(url, timeout=5)
    except Exception as e:
        raise e
    if response.status_code != 200:
        raise Exception(response.text)
    return response.json()
