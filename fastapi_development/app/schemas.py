
from pydantic import BaseModel,Field,EmailStr,AnyUrl,field_validator,model_validator,computed_field
from typing import Annotated,List,Literal,Optional
from uuid import UUID,uuid4
from datetime import datetime


class DimensionCM(BaseModel):
    length:Annotated[float,Field(default=0,strict=True,description="Length in cm")]
    width:Annotated[float,Field(default=0,strict=True,description="Width in cm")]
    height:Annotated[float,Field(default=0,strict=True,description="Height in cm")]


class Seller(BaseModel):
    id:UUID
    name:Annotated[
        str,
        Field(min_length=5,
              max_length=60,
              description="Valid Seller Name"
              )
    ]
    email:str
    website:AnyUrl
    
    @field_validator("email",mode="after")
    @classmethod
    def validate_seller_email_address(cls,value:str):
        allowed_domains = {
            "mistore.in",
            "realmeofficial.in",
            "samsungindia.in",
            "lenovostore.in",
            "hpworld.in",
            "applestoreindia.in",
            "dellexclusive.in",
            "sonycenter.in",
            "oneplusstore.in",
            "asusexclusive.in",
            "clothes.com"
        }
        
        domain = value.split("@")[-1].lower()
        if domain not in allowed_domains:
            raise ValueError("domain is not allowed")
        
        return value
    


class Product(BaseModel):
    id:UUID
    sku:Annotated[str,Field(
        min_length=6,
        max_length=30,
        description="Stock Keeping Unit",
        examples=["XIAO-359GB-001","REAL-135GB-002"]
    )]
    name:Annotated[str,Field(
        min_length=2,
        max_length=80,
        description="Readable Product Name with (2-80) character length"
    )]
    description:Annotated[str,Field(
        max_length=200,
        description="Short Product description"
    )]
    category:Annotated[str,Field(
        min_length=5,
        max_length=50,
        description="Valid Product Category",
        examples=["Mobiles","Shirts"]
    )]
    brand:Annotated[str,Field(
        min_length=2,
        max_length=50,
        description="Valid Product Brand",
        examples=["Xiaomi","Apple"]
    )]
    price:Annotated[float,Field(gt=0,strict=True,description="Base Price(INR)")]
    discount_percent:Annotated[float,Field(ge=0,le=90,description="Product discount %(INR)")]
    stock:Annotated[int,Field(ge=0,description="Product In stock")]
    is_active:Annotated[bool,Field(description="Is Product Active")]
    ratings:Annotated[
        float,
        Field(ge=0,le=5,strict=True,description="Product Rating")
    ]
    tags:Annotated[
        Optional[List[str]],
        Field(default=None,max_length=10,description="UP to 10 tags")
    ]
    
    image_urls:Annotated[
        List[AnyUrl],
        Field(max_length=10,min_length=1,description="At least 1 Image Urls")
    ]
    dimension_cm:DimensionCM
    seller:Seller
    created_at:Annotated[datetime,
            Field
            (
            default_factory=
            datetime.now
            )]    
    
    @field_validator("sku",mode="after")
    @classmethod
    def validate_sku(cls,value:str):
        if "-" not in value:
            raise ValueError("SKU must have -")
        
        last = value.split("-")[-1]
        
        if not (len(last) == 3 and last.isdigit()):
            raise ValueError("SKU must end with 3 digits at the end")
        
        return value
    
    @model_validator(mode="after")
    @classmethod
    def business_rules(cls,model:"Product"):
        if model.stock == 0 and model.is_active:
            raise ValueError("If stock is 0, then product must be In-Active")
        
        if model.discount_percent > 0 and model.ratings == 0:
            raise ValueError("Discounted product must have ratings given")
        
        return model
    
    
    @computed_field
    @property
    def final_price(self)->float:
        return round(self.price * (1 - self.discount_percent/100),2)
    
    
    @computed_field
    @property
    def computed_volume(self) -> float:
        d = self.dimension_cm
        return d.length * d.width * d.height
        
    