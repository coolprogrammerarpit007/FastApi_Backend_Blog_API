from pydantic import BaseModel,ValidationError,Field,EmailStr,HttpUrl,SecretStr,field_validator,model_validator,ValidationInfo,computed_field,ConfigDict
from datetime import datetime,UTC
from uuid import UUID,uuid4
from typing import Literal,Annotated
import re
import json

class User(BaseModel):
    # to accept data both as field name and alias
    model_config=ConfigDict(populate_by_name=True,str=True)
    # uid:Annotated[int,Field(gt=0)] = 786
    uid:UUID = Field(alias="id",default_factory=uuid4)
    name:Annotated[str,Field(min_length=3,max_length=20)]
    # email:str
    age:Annotated[int,Field(ge=18,le=60)]
    email:EmailStr
    password:SecretStr
    website:HttpUrl|None = None
    verified_at : datetime | None = None
    bio:str = ""
    is_active:bool = True
    full_name:str | None = None
    
    ### Computed Fields
    first_name: str = ""
    last_name: str = ""
    follower_count: int = 0
    
    
    @computed_field
    @property
    def display_name(self) -> str:
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.name

    @computed_field
    @property
    def is_influencer(self) -> bool:
        return self.follower_count >= 10000

    
    # custom validation to check username should be only alpha-numeric or contain _
    @field_validator("name")
    @classmethod
    def validator_username(cls,value:str)->str:
        if not value.replace("_", "").isalnum():
            raise ValueError("Username must be alpha-numeric (underscore allowed)")
        
        return value.lower()
    
    # mode to tell pydantic to run custom validation before basic/main validations
    @field_validator("website",mode="before")
    @classmethod
    def add_https(cls,value:str|None=None) -> str | None:
        if value and not value.startswith(("http://","https://")):
            return f"http://{value}"
        
        return value
        
        
class Comment(BaseModel):
    content: str
    author_email: EmailStr
    likes: int = 0
    
    
#  Unions (|) can be used to say field can be of many types
user1 = User(uid = 789,name="Arpit Mishra",email="arpit.mishra.out@gmail.com",age=25)

#  to validate data coming from API
user_data = {
    "id": "3bc4bf25-1b73-44da-9078-f2bb310c7374",
    "username": "Corey_Schafer",
    "email": "CoreyMSchafer@gmail.com",
    "age": "39",
    "password": "secret123",
}
user = User.model_validate_json(json.dumps(user_data))


class UserRegistration(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str
    
    @model_validator(mode='after')
    def passwords_match(self) -> 'UserRegistration':
        if self.password != self.confirm_password:
            raise ValueError('Passwords do not match')
        return self

try:
    registration = UserRegistration(
        email="CoreyMSchafer@gmail.com",
        password="secret123",
        confirm_password="secret456"
    )
except ValidationError as e:
    print(e)
# print(user1)


class BlogPost(BaseModel):
    title:str
    content:str
    view_count : int = 0
    is_published:bool = False
    
    tags:list[str] = Field(default_factory=list)
    created_at:datetime = Field(default_factory=lambda:datetime.now(tz=UTC))
    # author_id:str|int
    author:User
    status:Literal["draft","published","archived"] = "draft"
    slug:Annotated[str,Field(pattern=r"^[a-z0-9-]+$")]
    comments:list[Comment] = Field(default_factory=list)
    

#  on model re-assignment validation not re-work


# dictionary representation of model

print(user1.model_dump())

#  json representation of the user model
print(user1.model_dump_json(indent=2))


# *************************************************

# field validators are used to validate individual fields whereas model validators are used to validate complete models and properties of the model in the model validators instead of value self is used