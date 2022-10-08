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
        self.assertEqual(CPCNode("A", self.tree).level, 0)
        self.assertEqual(CPCNode("A24", self.tree).level, 1)
        self.assertEqual(CPCNode("A24D", self.tree).level, 2)
        self.assertEqual(CPCNode("A24D3/00", self.tree).level, 3)
        self.assertEqual(CPCNode("A24D3/02", self.tree).level, 4)
        self.assertEqual(CPCNode("A24D3/0204", self.tree).level, 5)
        self.assertEqual(CPCNode("A24D3/0208", self.tree).level, 6)
        self.assertEqual(CPCNode("A24D3/0216", self.tree).level, 7)
        

if __name__ == "__main__":
    unittest.main()
