from fastapi import FastAPI,Query,Path,HTTPException 
from services.product import get_all_products,add_product,remove,change_product
from schemas import Product,ProductUpdate
import json
from uuid import UUID,uuid4
from datetime import datetime

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
    
    
# get product by Id API

@app.get("/products/{id}")

def get_product_by_id(id:str=Path(
    ...,
    min_length=36,
    max_length=36,
    description="Valid Product Id with length of 36 chars"
)):
    products = get_all_products()
    
    product = [product for product in products if product["id"] == id]
    
    if not product:
        raise HTTPException(status_code=404,detail="Product not found!")
    
    return product[0]
        
        
    
    
@app.post("/products",status_code=201)

def create_new_product(product:Product):
    # convert it into dictionary to doing any modifications
    product_dict = product.model_dump(mode="json")
    product_dict["id"] = str(uuid4())
    product_dict["created_at"] = datetime.utcnow().isoformat() + "Z"
    try:
        add_product(product_dict)
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return product.model_dump(mode="json")


@app.delete("/products/{id}")

def remove_product(id:UUID = Path(
    ...,
    description="Product Id with a valid string"
)):
    try:
        print(id)
        res = remove(str(id))
        return res
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
# Update Product Inventory API

@app.put("/products/{id}")

def update_inventory_product(id:UUID=Path(
    ...,
    description="Valid Product Id"
),
                             payload:ProductUpdate=...,
                             ):
    try:
        update_product = change_product(
            str(id),payload.model_dump(mode="json",exclude_unset=True)
        )
        
        return update_product
        
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


        