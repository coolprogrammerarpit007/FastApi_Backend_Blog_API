from fastapi import FastAPI,HTTPException,Query,Path
from services.product import get_all_products
from schemas import Product

app = FastAPI()

@app.get("/")

def root():
    return {"message":"Welcome to FastAPI"}


# @app.get("/products/{id}")

# def get_products(id:int):
#     return {"message":f"Product with the {id} fetched successfully!"}
# @app.get("/products")

# def get_products():
#     return get_all_products()



        
@app.get("/products")

def fetch_product(name:str = Query(default=None,min_length=2,max_length=50,description="enter product name"),sort_by_price:bool = Query(default=False,description="sort products by price"),order:str=Query(default="asc",description="sort products by ascending or descending order"),limit:int = Query(default=5,ge=1,le=100,description="Number of Items to return"),offset:int = Query(default=0,ge=0,description="Pagination Offset")):
    if not name:
        return {
            "status":True,
            "message":"ALL products are given",
            "data":get_all_products()
        }
        
    products = get_all_products()
    
    
    product_name = name.strip().lower()
        
    if len(products) > 1:
        products = [product for product in products if product_name in product.get("name","").lower()]
        
        
        
    if not products:
        raise HTTPException(status_code=404,detail="No Products are found!")
    
    if sort_by_price:
        reverse = order == "desc"
        products = sorted(products,key=lambda product:product.get("price",0),reverse=reverse)
        
        
    return {
            "status":True,
            "message":"Products fetched successfully!",
            "total_products":len(products),
            "data" : products[offset:limit+offset],
        }
    
    
    
@app.get("/product/{id}")

def get_product_detail(id:str = Path(...,min_length=36,max_length=36,description="UUID of the product")):
    products = get_all_products()
    
    product = [product for product in products if product["id"] == id][0]
    
    if not product:
        raise HTTPException(status_code=404,detail="Product Not Found!")
    
    return {
        "status":True,
        "message":"Product found!",
        "data":product
    }
    
    
@app.post("/products",status_code=201)

def create_product(product:Product):
    pass