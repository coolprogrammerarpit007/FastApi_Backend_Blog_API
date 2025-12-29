from fastapi import FastAPI,Depends,status,Response,HTTPException
from schemas import Blog,ShowBlog,UserBase,ShowUser,UserCreate
import models
from database import engine,SessionLocal
from sqlalchemy.orm import Session
from typing import List
from passlib.context import CryptContext



app = FastAPI()

#  this will automatically create table when application runs
models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
        
    finally:
        db.close()

    
    

    
@app.post("/blogs",status_code=status.HTTP_201_CREATED)

def create_blog(blog:Blog,db:Session = Depends(get_db)):
    new_blog = models.Blog(title=blog.title,body=blog.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.delete("/blogs/{id}",status_code=status.HTTP_204_NO_CONTENT)

def destroy(id,db:Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session = False)
    db.commit()
    return {"message":f"Blog with the {id} deleted successfully!"}


@app.put("/blogs/{id}",status_code=status.HTTP_202_ACCEPTED)

def update_blog(id: int, blog: Blog, db: Session = Depends(get_db)):
    db_blog_query = db.query(models.Blog).filter(models.Blog.id == id)
    
    if not db_blog_query.first():
        raise HTTPException(status_code=404, detail="Blog not found!")
    
    updated_count = db_blog_query.update(
        {"title": blog.title, "body": blog.body},
        synchronize_session=False
    )
    
    db.commit()
    
    # To return the updated data, re-query it
    updated_blog = db_blog_query.first()
    
    return {
        "msg": "blog updated successfully!",
        "data": updated_blog
    }
    

@app.get("/blogs",status_code=200)

def get_all_blogs(db:Session=Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get("/blog/{id}",status_code=200,response_model=ShowBlog)

def get_blog_details(id:int,response:Response,db:Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"Blog with {id} is not available!"
    return ShowBlog(
        status=True,
        title=blog.title,
        body = blog.body
    )
    
    
# ************************  User API ***********************

pwd_cxt = CryptContext(schemes=["bcrypt"],deprecated="auto")
@app.post("/user",status_code=201,response_model=ShowUser)

def create_user(user:UserCreate,db:Session = Depends(get_db)):
    # check if user already exist
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    # Hashed Password   
    hashed_password = pwd_cxt.hash(user.password)
    
    #  create new user
    new_user = models.User(name=user.name,email=user.email,password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return ShowUser(
        name=user.name,
        email=user.email,
        status=True  # or compute it based on some logic
    )

@app.get("/user/{id}",response_model=ShowUser)


def get_user_Details(id:int,db:Session = Depends(get_db)):
    user_details = db.query(models.User).filter(models.User.id == id).first()
    
    if not user_details:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,details="User not found!")
    
    return ShowUser(
        id=user_details.id,
        name=user_details.name,
        email=user_details.email,
        status=True  # or compute it based on some logic
    )