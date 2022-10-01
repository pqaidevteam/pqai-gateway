import sys
import unittest
from pathlib import Path
from fastapi.testclient import TestClient

TEST_DIR = Path(__file__).resolve().parent
BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.append(BASE_DIR.as_posix())

from main import app

class TestServer(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)
        self.client.testing = True

    def test__search_route(self):
        payload = {
            "query": "Sound suppression means in a drone",
            "before": "2020-01-01",
            "after": "2010-12-31",
            "n": 10,
            "rerank": False
        }
        response = self.client.post('/search', json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("query", data)
        self.assertIsInstance(data["query"], str)
        self.assertSearchResultResponse(data)
    
    def test__similar_route(self):
        response = self.client.get('/patents/US7654321B2/similar')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertSearchResultResponse(data)

    def test__prior_art_route(self):
        response = self.client.get('/patents/US7654321B2/claims/1/prior-art')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertSearchResultResponse(data)
    
    def assertSearchResultResponse(self, data):
        self.assertIn("results", data)
        self.assertIsInstance(data["results"], list)
        self.assertGreater(len(data["results"]), 0)

        for result in data["results"]:
            self.assertIn("doc_id", result)
            self.assertIsInstance(result["doc_id"], str)
            
            self.assertIn("title", result)
            self.assertIsInstance(result["title"], str)
            
            self.assertIn("abstract", result)
            self.assertIsInstance(result["abstract"], str)
            
            self.assertIn("publication_date", result)
            self.assertIsInstance(result["publication_date"], str)
            self.assertRegex(result["publication_date"], r"\d{4}-\d{2}-\d{2}")

            self.assertIn("score", result)
            self.assertIsInstance(result["score"], float)


if __name__ == "__main__":
    unittest.main()
