import sys
import json
from pathlib import Path
from fastapi import APIRouter, Response

THIS_DIR = Path(__file__).resolve().parent
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(THIS_DIR.as_posix())
sys.path.append(BASE_DIR.as_posix())

from cpcscheme import CPCTree, CPCNode

CPC_DATA_FILE = str(THIS_DIR / "assets/cpc_data.json")
with open(CPC_DATA_FILE, "r", encoding="utf-8") as f:
    data = [json.loads(line) for line in f]
    cpc_tree = CPCTree(data)

router = APIRouter()

@router.get('/cpcs/{cpc}')
async def get_cpc_data(cpc: str):
    if cpc not in cpc_tree:
        return Response(status_code=404, content="Invalid CPC code")

@router.get('/cpcs/{cpc}/definition')
async def get_definition(cpc: str):
    if cpc not in cpc_tree:
        return Response(status_code=404, content="Invalid CPC code")

@router.get('/cpcs/{cpc}/subtree')
async def get_subtree(cpc: str):
    if cpc not in cpc_tree:
        return Response(status_code=404, content="Invalid CPC code")

