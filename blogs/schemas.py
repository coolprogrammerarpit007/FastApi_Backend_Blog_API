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
    
    