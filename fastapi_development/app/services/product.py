from pathlib import Path
import json
from typing import List,Dict

DATA_FILE = Path(".","data","products.json")
print(DATA_FILE)

def all_products() ->List[dict]:
    if not DATA_FILE.exists():
        return []
    
    with open(DATA_FILE,"r",encoding="utf-8") as File:
        return json.load(File)
    
def get_all_products() ->List[Dict]:
    return all_products()