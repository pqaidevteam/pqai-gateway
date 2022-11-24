import unittest
import sys
from pathlib import Path
import numpy as np
from dotenv import load_dotenv

TEST_DIR = Path(__file__).resolve().parent
BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.append(BASE_DIR.as_posix())

env_file = BASE_DIR / ".env"
load_dotenv(env_file.as_posix())

from core.encoder_srv import encode
from core.db_srv import get_document
from core.index_srv import vector_search

class TestServices(unittest.TestCase):

    def test_encoder_service(self):
        test_string = "test string"
        vector = encode(test_string, "sbert")
        self.assertIsInstance(vector, list)
        self.assertTrue(all(isinstance(e, float) for e in vector))

    def test_classifier_service(self):
        pass

    def test_db_service(self):
        doc = get_document("US7654321B2")
        self.assertIsInstance(doc, dict)
        self.assertGreater(len(doc.keys()), 0)

    def test_index_service(self):
        vec = tuple(np.random.random(768))
        results = vector_search(vec, 10)
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 10)

    def test_reranker_service(self):
        pass

    def test_snippet_service(self):
        pass

if __name__ == "__main__":
    unittest.main()
