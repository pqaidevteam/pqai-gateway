"""
Classes that model the CPC tree and nodes
"""

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class CPCTree(metaclass=Singleton):

    def __init__(self, data: list):
        """Initialize the tree with the data
        
        Args:
            data (list): List of dictionaries with the following keys: `symbol`, `parents`
        """
        self._tree = self._create_tree(data)
        self._roots = ["A", "B", "C", "D", "E", "F", "G", "H", "Y"]
    
    def _create_tree(self, data: list):
        tree = {}
        for row in data:
            symbol = row["symbol"]
            if symbol not in tree:
                tree[symbol] = {"parent": None, "children": []}
            tree[symbol]["definition"] = row["title_full"]
            if not row["parents"]:
                continue
            parent = row["parents"][0]
            tree[symbol]["parent"] = parent
            if parent not in tree:
                tree[parent] = {"parent": None, "children": []}
            tree[parent]["children"].append(symbol)
        return tree
    
    def __contains__(self, code: str):
        return code in self._tree
    
    @property
    def sections(self):
        return [CPCNode(code, self) for code in self._roots]
    
    def get_children(self, code: str):
        if code not in self:
            raise ValueError(f"Invalid code: {code}")
        return self._tree[code]["children"]
    
    def get_parent(self, code: str):
        if code not in self:
            raise ValueError(f"Invalid code: {code}")
        return self._tree[code]["parent"]
    
    def get_definition(self, code: str):
        if code not in self:
            raise ValueError(f"Invalid code: {code}")
        return self._tree[code]["definition"]


class CPCNode:

    def __init__(self, code: str, tree: CPCTree):
        assert code in tree, f"CPC {code} not found in CPC tree"
        self.code = code
        self.tree = tree

    def __repr__(self):
        return f"<CPCNode {self.code}>"
    
    def __str__(self):
        return self.code
    
    @property
    def parent(self):
        p = self.tree.get_parent(self.code)
        if p is None:
            return None
        return CPCNode(p, self.tree)
    
    @property
    def children(self):
        arr = self.tree.get_children(self.code)
        if not arr:
            return []
        return [CPCNode(c, self.tree) for c in arr]
    
    @property
    def level(self):
        if self.parent is None:
            return 0
        return self.parent.level + 1

    @property
    def definition(self):
        return self.tree.get_definition(self.code)
