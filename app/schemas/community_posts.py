from typing import Optional,List
from pydantic import BaseModel
from datetime import datetime


class CommunityPostCreate(BaseModel):
    post_title:str
    post_content:str

class AddCommunityPostComment(BaseModel):
    post_id:int
    comment:str
    
class CommunityPostReactions(BaseModel):
    post_id:int
    

class GetCommunityPost(BaseModel):
    id: int
    student_id: int
    post_title: str
    post_content: str
    post_date: Optional[datetime] = None
    likes_count: int
    comments_count: int

    class Config:
        orm_mode = True
    