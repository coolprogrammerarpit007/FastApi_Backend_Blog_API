from pydantic import BaseModel,ConfigDict,EmailStr
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
    email:EmailStr
    
    
class UserCreate(UserBase): # Used when creating a user
    password:str
    
    
class ShowUser(UserBase): # what we return to the user
    # id:Optional[int] = None
    status:bool
    
    model_config = ConfigDict(from_attributes=True)
    
    
# NEW TOKEN SCHEMAS

class Token(BaseModel):
    access_token:str
    token_type:str
    
class TokenData(BaseModel):
    email:Optional[str] = None
    
    
class LoginResponse(BaseModel):
    status:bool
    message:str
    access_token:str
    token_type:str = "bearer"
    
    