from typing import Optional
from pydantic import BaseModel,EmailStr,HttpUrl


class StudentRegister(BaseModel):
    student_name: str
    student_email: EmailStr
    personal_email: EmailStr
    password: str
    student_bio: Optional[str] = None
    # profile_picture: Optional[HttpUrl] = None
    github_url: str = None
    leetcode_url: str = None
    codeforces_url: str = None
    hackerrank_url: str = None
    portfolio_website_url: str = None


class StudentLogin(BaseModel):
    student_email: EmailStr
    password: str



class StudentUpdate(BaseModel):
    student_name: Optional[str] = None
    personal_email: Optional[EmailStr] = None
    student_bio: Optional[str] = None
    password: str
    # profile_picture: Optional[HttpUrl] = None
    github_url: str = None
    leetcode_url: str = None
    codeforces_url: str = None
    hackerrank_url: str = None
    portfolio_website_url: str = None


class StudentGet(BaseModel):
    id: int
    student_name: str
    student_email: EmailStr
    personal_email: EmailStr
    student_bio: Optional[str]
    # profile_picture: Optional[str]
    github_url: str = None
    leetcode_url: str = None
    codeforces_url: str = None
    hackerrank_url: str = None
    portfolio_website_url: str = None

    model_config = {
        "from_attributes": True
    }