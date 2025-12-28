from database import Base
from sqlalchemy import Column,Integer,String,Float

class Blog(Base):
    __tablename__ = 'blogs'
    id = Column(Integer,primary_key=True,index=True)
    title=Column(String(50))
    body = Column(String(255))
    
    
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True,index=True)
    name=Column(String(70))
    email = Column(String(50))
    password = Column(String(255))