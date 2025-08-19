import datetime
from sqlalchemy import Column,Integer,String,ForeignKey,DateTime
from app.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime


class Community_Posts(Base):
    __tablename__="community_posts"
    id=Column(Integer,primary_key=True,index=True)
    student_id=Column(Integer,ForeignKey("students.id"),nullable=False)
    post_title=Column(String,nullable=True)
    post_content=Column(String,nullable=False)
    post_date=Column(DateTime,default=datetime.utcnow)

    # relationships

    student_info=relationship("Student",back_populates="posts")
    comments=relationship("Community_Posts_Comments",back_populates="post_info",cascade="all,delete-orphan")
    likes=relationship("Community_Posts_Likes",back_populates="post_info",cascade="all,delete-orphan")





class Community_Posts_Comments(Base):
    __tablename__="community_posts_comments"
    id=Column(Integer,primary_key=True,index=True)
    post_id=Column(Integer,ForeignKey("community_posts.id"),nullable=False)
    student_id=Column(Integer,ForeignKey("students.id"),nullable=False)
    comment=Column(String,nullable=False)
    comment_date=Column(DateTime,default=datetime.utcnow)

    # relationships
    post_info=relationship("Community_Posts",back_populates="comments")
    



class Community_Posts_Likes(Base):
    __tablename__="community_posts_likes"
    id=Column(Integer,primary_key=True,index=True)
    post_id=Column(Integer,ForeignKey("community_posts.id"),nullable=False)
    student_id=Column(Integer,ForeignKey("students.id"),nullable=False)

    # relationships
    post_info=relationship("Community_Posts",back_populates="likes")
    student_info=relationship("Student",back_populates="likes")
