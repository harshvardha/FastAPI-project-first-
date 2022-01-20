from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def index():
    return {
        "data": {
            "name": "Harshvardhan Singh Chauhan"
        }
    }


@app.get("/blog")
def fetchBlog(limit: int = 10, published: bool = True, sort: Optional[str] = None):
    # If no limit is given then fetch 10 blogs at once
    # If limit is given then use that to fetch the blogs
    if(published):
        return {
            "data": f"{limit} published blogs from the db"
        }
    else:
        return {
            "data": f"{limit} blogs from the db"
        }


@app.get("/blog/{id}")
def about(id: int):
    return {
        "blog_id": id
    }


@app.get("/blog/{id}/comments")
def comments(id: int):
    return {
        "comments": id
    }


class BlogSchema(BaseModel):
    title: str
    body: str
    published: Optional[bool]


@app.post("/blog")
def createBlog(blog: BlogSchema):
    return {
        "data": f"Blog is created and saved with title as {blog.title}"
    }
