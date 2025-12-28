from pydantic import BaseModel
from typing import Optional

class Blog(BaseModel):
    title:str
    body:Optional[str] = None
    
    class Config:
        from_attributes = True  # allows returning SQLAlchemy models directly
        
class ShowBlog(Blog):
    status:bool
    title:str
    body:str
    
    
    
    
class User(BaseModel):
    name:str
    email:str
    password:str
    
class ShowUser(User):
    status:True
    name:str
    email:str