from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional


app = FastAPI()

class Blog(BaseModel):
    title:str
    body:str
    published_at:Optional[bool]
    

@app.get("/")

def read_root():
    return {
        "message":"welcome to blog Api!"
    }
    
@app.get("/blogs")

def get_all_blogs(limit:int=10,published:bool=True,sort:Optional[str]=None):
    if published:
        return {"data": f"{limit} published blogs from the server"}
    else:
        return {"data":"Unpublished blogs from the server"}
    
@app.post("/blogs")
def create_blog(blog:Blog):
    return {
        "msg":f"blog has been created with {blog.title}"
    }