from pydantic import BaseModel

from .base import CommonAttrs




class PostCreate(BaseModel):
    title: str
    content: str
    user_id: str

class PostUpdate(BaseModel):
    title: str
    content: str
    

class Post(CommonAttrs):    
    title: str
    content: str
    

