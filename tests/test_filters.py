import sys
import unittest
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.append(BASE_DIR.as_posix())
env_file = BASE_DIR / ".env"
load_dotenv(env_file.as_posix())

from core.documents import Document
from plugins.search.filters import PublicationDateFilter

class TestFilters(unittest.TestCase):

    def setUp(self):
        self.doc1 = Document("US7654321B2") # published 2010-02-02
        self.doc2 = Document("US10112730B2") # published 2018-10-30
        self.docs = [self.doc1, self.doc2]

    def test__publication_date_filter(self):
        df = PublicationDateFilter(None, "2010-01-01")
        self.assertFalse(df(self.doc1))
        self.assertFalse(df(self.doc2))
        self.assertEqual(len(df.apply(self.docs)), 0)

        df = PublicationDateFilter(None, "2015-01-01")
        self.assertTrue(df(self.doc1))
        self.assertFalse(df(self.doc2))
        self.assertEqual(len(df.apply(self.docs)), 1)

        df = PublicationDateFilter(None, "2020-01-01")
        self.assertTrue(df(self.doc1))
        self.assertTrue(df(self.doc2))
        self.assertEqual(len(df.apply(self.docs)), 2)

        df = PublicationDateFilter("2010-01-01", None)
        self.assertTrue(df(self.doc1))
        self.assertTrue(df(self.doc2))
        self.assertEqual(len(df.apply(self.docs)), 2)

        df = PublicationDateFilter("2015-01-01", None)
        self.assertFalse(df(self.doc1))
        self.assertTrue(df(self.doc2))
        self.assertEqual(len(df.apply(self.docs)), 1)

        df = PublicationDateFilter("2020-01-01", None)
        self.assertFalse(df(self.doc1))
        self.assertFalse(df(self.doc2))
        self.assertEqual(len(df.apply(self.docs)), 0)

        df = PublicationDateFilter("2005-01-01", "2010-01-01")
        self.assertFalse(df(self.doc2))
        self.assertFalse(df(self.doc1))
        self.assertEqual(len(df.apply(self.docs)), 0)

        df = PublicationDateFilter("2010-01-01", "2020-01-01")
        self.assertTrue(df(self.doc1))
        self.assertTrue(df(self.doc2))
        self.assertEqual(len(df.apply(self.docs)), 2)

        df = PublicationDateFilter("2010-01-01", "2015-01-01")
        self.assertTrue(df(self.doc1))
        self.assertFalse(df(self.doc2))
        self.assertEqual(len(df.apply(self.docs)), 1)

        df = PublicationDateFilter("2015-01-01", "2020-01-01")
        self.assertFalse(df(self.doc1))
        self.assertTrue(df(self.doc2))
        self.assertEqual(len(df.apply(self.docs)), 1)

        df = PublicationDateFilter("2020-01-01", "2025-01-01")
        self.assertFalse(df(self.doc1))
        self.assertFalse(df(self.doc2))
        self.assertEqual(len(df.apply(self.docs)), 0)

        df = PublicationDateFilter(None, None)
        self.assertTrue(df(self.doc1))
        self.assertTrue(df(self.doc2))
        self.assertEqual(len(df.apply(self.docs)), 2)
        

if __name__ == "__main__":
    unittest.main()
