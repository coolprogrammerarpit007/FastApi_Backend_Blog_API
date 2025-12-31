import json
from pathlib import Path
from typing import List,Dict

DATA_FILE = Path(".","data","products.json")

def load_product() -> List[Dict]:
    if not DATA_FILE.exists():
        return []
    
    with open(DATA_FILE,"r",encoding='utf-8') as file:
        return json.load(file)
    
    
def get_all_products() -> List[Dict]:
    return load_product()