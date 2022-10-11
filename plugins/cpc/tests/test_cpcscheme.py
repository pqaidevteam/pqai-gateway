import sys
import unittest
import json
from pathlib import Path
from dotenv import load_dotenv

TEST_DIR = Path(__file__).resolve().parent.parent

sys.path.append(TEST_DIR.as_posix())
env_file = TEST_DIR / ".env"

load_dotenv(env_file.as_posix())

from cpcscheme import CPCNode, CPCTree

class TestCPCScheme(unittest.TestCase):

    def setUp(self):
        cpc_data_file_path = TEST_DIR / "assets/cpc_data.json"
        cpc_data = []
        with open(cpc_data_file_path, "r", encoding="utf-8") as f:
            for line in f:
                cpc_data.append(json.loads(line))
        self.cpc_tree = CPCTree(cpc_data)
    
    def test__can_return_children(self):
        children = self.cpc_tree.get_children("A01B")
        self.assertIsInstance(children, list)
        self.assertEqual(len(children), 37)
        self.assertCountEqual(children, set(children))
    
    def test__can_return_parent(self):
        parent = self.cpc_tree.get_parent("A01B")
        self.assertEqual(parent, "A01")
    
    def test__raises_error_for_invalid_cpc(self):
        invalid_cpc = "A31"
        with self.assertRaises(ValueError):
            self.cpc_tree.get_children(invalid_cpc)
        with self.assertRaises(ValueError):
            self.cpc_tree.get_parent(invalid_cpc)
        
    def test__can_return_sections(self):
        sections = self.cpc_tree.sections
        self.assertIsInstance(sections, list)
        self.assertEqual(len(sections), 9)
        self.assertTrue(isinstance(s, CPCNode) for s in sections)
    
    def test__can_return_definition(self):
        code = "A"
        definition = self.cpc_tree.get_definition(code)
        self.assertEqual(definition, "HUMAN NECESSITIES")
        codes = ["A", "A24", "A24D", "A24D3/00", "A24D3/02",
                 "A24D3/0204", "A24D3/0208", "A24D3/0216"]
        for code in codes:
            self.assertIsInstance(self.cpc_tree.get_definition(code), str)


class TestCPCNode(unittest.TestCase):

    def setUp(self):
        cpc_data_file_path = TEST_DIR / "assets/cpc_data.json"
        cpc_data = []
        with open(cpc_data_file_path, "r", encoding="utf-8") as f:
            for line in f:
                cpc_data.append(json.loads(line))
        self.tree = CPCTree(cpc_data)
    
    def test__can_initialize(self):
        node = CPCNode("A01B", self.tree)
        self.assertIsInstance(node, CPCNode)
    
    def test__can_return_children(self):
        node = CPCNode("A01B", self.tree)
        self.assertIsInstance(node.children, list)
        self.assertEqual(len(node.children), 37)
        self.assertTrue(isinstance(child, CPCNode) for child in node.children)
    
    def test__can_return_parent(self):
        node = CPCNode("A01B", self.tree)
        self.assertIsInstance(node.parent, CPCNode)
    
    def test__can_convert_to_string(self):
        node = CPCNode("A01B", self.tree)
        self.assertEqual(str(node), "A01B")
    
    def test__repr(self):
        node = CPCNode("A01B", self.tree)
        self.assertEqual(repr(node), "<CPCNode A01B>")
    
    def test__can_return_level(self):
        codes = ["A", "A24", "A24D", "A24D3/00", "A24D3/02",
                 "A24D3/0204", "A24D3/0208", "A24D3/0216"]
        for i, code in enumerate(codes):
            self.assertEqual(CPCNode(code, self.tree).level, i)
        
    def test__can_return_definition(self):
        node = CPCNode("A", self.tree)
        self.assertEqual(node.definition, "HUMAN NECESSITIES")
        codes = ["A", "A24", "A24D", "A24D3/00", "A24D3/02",
                 "A24D3/0204", "A24D3/0208", "A24D3/0216"]
        for code in codes:
            self.assertIsInstance(CPCNode(code, self.tree).definition, str)


if __name__ == "__main__":
    unittest.main()
