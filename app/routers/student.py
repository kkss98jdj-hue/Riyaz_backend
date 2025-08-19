from fastapi import APIRouter, Depends,Header
from sqlalchemy.orm import Session
from app.schemas.student import StudentRegister ,StudentLogin,StudentUpdate
from app.database import get_db
from app.crud.student import StudentHandler
from typing import Optional
from app.schemas.common import BaseResponse

router = APIRouter()
student_handler = StudentHandler()


@router.post("/registerstudent")
async def register_student(student: StudentRegister, db: Session = Depends(get_db)):
    return await student_handler.register_student(db=db, student_data=student.dict())



@router.post("/loginstudent")
async def login_student(student: StudentLogin, db: Session = Depends(get_db)):
    return await student_handler.login_student(db=db, login_data=student.dict())



@router.get("/getstudent")
async def get_student_details(
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(None)
):
    if not authorization or not authorization.startswith("Bearer "):
        return BaseResponse[None](
            Status="Failed",
            Message="Invalid or missing token",
            Data=None
        )
    token = authorization.split(" ")[1]
    return await student_handler.get_student_details(db=db, token=token)


@router.put("/updatestudent")
async def update_student(
    student: StudentUpdate,
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(None)
):
    if not authorization or not authorization.startswith("Bearer "):
        return BaseResponse[None](
            Status="Failed",
            Message="Invalid or missing token",
            Data=None
        )
    token = authorization.split(" ")[1]
    return await student_handler.update_student(
        db=db,
        token=token,
        student_data=student.dict(exclude_unset=True)
    )
