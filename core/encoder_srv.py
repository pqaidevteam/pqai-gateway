"""Encoder service"""

import os
from functools import lru_cache
import requests

ENCODER_SRV_ENDPOINT = os.environ["ENCODER_SRV_ENDPOINT"]

@lru_cache(maxsize=1024)
def encode(data, encoder):
    """Encode given data using given encoder"""
    payload = {"data": data, "encoder": encoder}
    url = f"{ENCODER_SRV_ENDPOINT}/encode"
    try:
        response = requests.post(url, json=payload, timeout=5)
    except Exception as e:
        raise e
    if response.status_code != 200:
        raise Exception(response.text)
    return response.json().get("encoded")
