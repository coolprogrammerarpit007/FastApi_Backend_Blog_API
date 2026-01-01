from fastapi import FastAPI,Query
from services.product import get_all_products
from schemas import Product
import json

app = FastAPI()

@app.get("/")

def create_root():
    return {
        "message":"Fastapi working smoothly, you can start working!"
    }
    
    



# API to load all the products
@app.get("/products",status_code=200)
def list_products(
    name:str = Query(default=None,
                     min_length=1,max_length=50,
                     description="Search Any Product by Name",
                     examples="Shirts"
                     ),
    sort_by_price:bool = Query(
        default=False,
        description="Sort products by price",
        examples=True
    ),
    order:str = Query(
        default="asc",
        description="Sort order when sort_by_price=True"
    ),
    limit:int = Query(
        default=10,
        ge=1,
        le=100,
        description="Number of items to return"
    ),
    offset:int = Query(
        default=0,
        ge=0,
        description="Product Offset"
    )
    ):
    products = get_all_products()

    if not name:
        return {
            "status":True,
            "message":"All products found",
            "products-data":products
        }
        
    product_item = name.strip().lower()
    products = [product for product in products if product_item in product.get("name","").lower()]
    
    message = f"Search results for {product_item}" if products else "No Item Found!"
    status = True if products else False
    
    if(products and sort_by_price):
        reverse = order == "desc"
        products = sorted(products,key=lambda product:product.get("price",0),reverse=reverse)
        
    if(limit):
        products = products[offset:limit+offset]
        
    total_products = len(products)
    return {
        "status":status,
        "message":message,
        "total_products":total_products,
        "limit":limit,
        "data":products
    }
        
    
    
@app.post("/products",status_code=201)

def create_new_product(product:Product):
    # convert it into dictionary to doing any modifications
    product_dict = product.model_dump()
    print(product_dict)
    return product