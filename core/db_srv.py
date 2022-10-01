import os
import requests

DB_SRV_ENDPOINT = os.environ["DB_SRV_ENDPOINT"]

def get_document(doc_id: str) -> dict:
    """Get document by id"""
    try:
        response = requests.get(f"{DB_SRV_ENDPOINT}/patents/{doc_id}")
    except Exception as e:
        raise e
    if response.status_code != 200:
        raise Exception(response.text)
    return response.json()
