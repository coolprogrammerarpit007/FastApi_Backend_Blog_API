from fastapi import FastAPI,Depends,status,Response
from schemas import Blog
import models
from database import engine,SessionLocal
from sqlalchemy.orm import Session


app = FastAPI()

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

@app.get("/blogs",status_code=200)

def get_all_blogs(db:Session=Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get("/blog/{id}",status_code=200)

def get_blog_details(id:int,response:Response,db:Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        response.status_code = status.HTTP_404_NOT_FOUND
        return f"Blog with {id} is not available!"
    return blog
    