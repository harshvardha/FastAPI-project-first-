from urllib import request
from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas, models
from . database import engine, sessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.base.metadata.create_all(bind=engine)


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/blog", status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    newBlog = models.Blog(title=request.title, body=request.body)
    db.add(newBlog)
    db.commit()
    db.refresh(newBlog)
    return newBlog


@app.get("/blog")
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get("/blog/{id}", status_code=status.HTTP_200_OK)
def show(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.uniqueId == id).first()
    if(not blog):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {id} is not available")
    return blog


@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.uniqueId ==
                                 id).delete(synchronize_session=False)
    db.commit()
    return "done"


@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.uniqueId == id)
    if(not blog):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} not found")
    blog.update(request)
    db.commit()
    return "updated"
