from fastapi import FastAPI,HTTPException,Query
from services.product import get_all_products

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

def fetch_product(name:str = Query(default=None,min_length=2,max_length=50,description="enter product name"),sort_by_price:bool = Query(default=False,description="sort products by price"),order:str=Query(default="asc",description="sort products by ascending or descending order")):
    if not name:
        return {
            "status":True,
            "message":"ALL products are given",
            "data":get_all_products()
        }
        
    products = get_all_products()
    
    
    product_name = name.strip().lower()
    if sort_by_price:
        reverse = order == "desc"
        products = sorted(products,key=lambda product:product.get("price",0),reverse=reverse)
        
    if len(products) > 1:
        products = [product for product in products if product_name in product.get("name","").lower()]
        
        return {
            "status":True,
            "message":"Products fetched successfully!",
            "total_products":len(products),
            "data" : products,
        }
        
    if not products:
        raise HTTPException(status_code=404,detail="No Products are found!")
    
    