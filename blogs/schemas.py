from pydantic import BaseModel,ConfigDict
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
    
    
    
    
class UserBase(BaseModel):  # Common Fields
    name:str
    email:str
    
    
class UserCreate(UserBase): # Used when creating a user
    password:str
    
    
class ShowUser(UserBase): # what we return to the user
    id:Optional[int] = None
    status:bool
    
    model_config = ConfigDict(from_attributes=True)
    