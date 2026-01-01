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

def save_product(products: List[Dict]) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)


def add_product(product:Dict) -> Dict:
    products = get_all_products()
    if any(p["sku"] == product["sku"] for p in products):
        raise ValueError("Product already exists!")
    
    products.append(product)
    save_product(products)
    return product