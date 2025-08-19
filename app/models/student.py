from sqlalchemy import Column,Integer,String,Boolean
from app.database import Base
from sqlalchemy.orm import relationship


class Student(Base):
    __tablename__="students"
    id= Column(Integer,primary_key=True,index=True)
    student_name=Column(String,index=True)
    student_email=Column(String,unique=True,index=True)
    personal_email=Column(String,unique=True,index=True)
    hashed_password=Column(String)
    student_bio=Column(String)
    # profile_picture=Column(String,nullable=True)
    github_url=Column(String,nullable=True)
    leetcode_url=Column(String,nullable=True)
    codeforces_url=Column(String,nullable=True)
    hackerrank_url=Column(String,nullable=True)
    portfolio_website_url=Column(String,nullable=True)
    

    #relationships with other tables/models
    posts=relationship("Community_Posts",back_populates="student_info",cascade="all,delete-orphan")
    likes=relationship("Community_Posts_Likes",back_populates="student_info",cascade="all,delete-orphan")
    # problems_solved=relationship("Problems_Solved",back_populates="student",cascade="all,delete-orphan")