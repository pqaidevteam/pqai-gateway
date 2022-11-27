"""Database service
"""

import os
import httpx

DB_SRV_ENDPOINT = os.environ["DB_SRV_ENDPOINT"]

async def get_document(doc_id: str) -> dict:
    """Get document by ID"""
    url = f"{DB_SRV_ENDPOINT}/patents/{doc_id}"
    async with httpx.AsyncClient() as client:
        timeout = httpx.Timeout(10.0, read=20.0)
        response = await client.get(url, timeout=timeout)
        return response.json()
