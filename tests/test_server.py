import sys
import unittest
from pathlib import Path
from fastapi.testclient import TestClient
from jsonschema import validate
import jsonschema

TEST_DIR = Path(__file__).resolve().parent
BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.append(BASE_DIR.as_posix())

from main import app

class TestServer(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)
        self.client.testing = True
        self.schema = {
            "type": "object",
            "properties": {
                "doc_id": {"type": "string"},
                "title": {"type": "string"},
                "abstract": {"type": "string"},
                "publication_date": {"type": "string"},
                "score": {"type": "number"},
            }
        }

    def test__search_102_route(self):
        payload = {
            "query": "Sound suppression means in a drone",
            "before": "2020-01-01",
            "after": "2010-12-31",
            "n": 10,
            "rerank": False
        }
        response = self.client.post('/search/102', json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertValidSearchResponse(response)

    def test__search_103_route(self):
        payload = {
            "query": "Sound suppression means in a drone"
        }
        response = self.client.post('/search/103', json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("query", data)
        self.assertIn("results", data)
        self.assertIsInstance(data["query"], str)
        self.assertIsInstance(data["results"], list)
        self.assertGreater(len(data["results"]), 0)
        for result1, results2 in data["results"]:
            try:
                validate(result1, self.schema)
                validate(results2, self.schema)
            except jsonschema.exceptions.ValidationError as e:
                self.fail(f"Invalid search result: {e}")

    def test__similar_route(self):
        response = self.client.get('/patents/US7654321B2/similar')
        self.assertEqual(response.status_code, 200)
        self.assertValidSearchResponse(response)

    def test__prior_art_route(self):
        response = self.client.get('/patents/US7654321B2/claims/1/prior-art')
        self.assertEqual(response.status_code, 200)
        self.assertValidSearchResponse(response)

    def assertValidSearchResponse(self, response):
        data = response.json()
        self.assertIn("query", data)
        self.assertIsInstance(data["query"], str)
        self.assertIn("results", data)
        self.assertIsInstance(data["results"], list)
        self.assertGreater(len(data["results"]), 0)
        for result in data["results"]:
            try:
                validate(result, self.schema)
            except jsonschema.exceptions.ValidationError as e:
                self.fail(f"Invalid search result: {e}")

if __name__ == "__main__":
    unittest.main()
