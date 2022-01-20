from sqlalchemy import Column, Integer, String
from . database import base


class Blog(base):
    __tablename__ = "blogs"
    uniqueId = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
