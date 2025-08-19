from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.student import Student as StudentModel
from app.schemas.common import BaseResponse
from app.schemas.student import StudentGet
from app.routers.auth import AuthHandler


class StudentHandler:

    async def register_student(self, db: Session, student_data: dict):
        try:
            # Check if email already exists
            existing_student = db.query(StudentModel).filter(
                StudentModel.student_email == student_data.get("student_email")
            ).first()

            if existing_student:
                return BaseResponse[None](
                    Status="Failed",
                    Message="Student with this student email already exists",
                    Data=None
                )

            # Hash the password before storing
            hashed_password = AuthHandler({"password": student_data.pop("password")}).get_password_hash()
            student_data["hashed_password"] = hashed_password

            # Create new student
            new_student = StudentModel(**student_data)
            db.add(new_student)
            db.commit()
            db.refresh(new_student)

            return BaseResponse[StudentGet](
                Status="Success",
                Message="Student registered successfully",
                Data=StudentGet.from_orm(new_student)
            )

        except SQLAlchemyError as e:
            db.rollback()
            return BaseResponse[None](
                Status="Failed",
                Message=f"Database error: {str(e)}",
                Data=None
            )
        except Exception as e:
            return BaseResponse[None](
                Status="Failed",
                Message=f"Unexpected error: {str(e)}",
                Data=None
            )
        
        
    
    async def login_student(self, db: Session, login_data: dict):
        try:
            # Check if student exists
            student = db.query(StudentModel).filter(
                StudentModel.student_email == login_data.get("student_email")
            ).first()

            if not student:
                return BaseResponse[None](
                    Status="Failed",
                    Message="Invalid email",
                    Data=None
                )

            # Verify password
            is_valid = AuthHandler({
                "password": login_data.get("password"),
                "hashed_password": student.hashed_password
            }).verify_password()

            if not is_valid:
                return BaseResponse[None](
                    Status="Failed",
                    Message="Invalid password",
                    Data=None
                )

            # Create JWT token
            token = AuthHandler({
                "sub": str(student.id),
                "email": student.student_email
            }).create_access_token()

            return BaseResponse[dict](
                Status="Success",
                Message="Login successful",
                Data={
                    "token": token,
                    "student": StudentGet.from_orm(student)
                }
            )

        except SQLAlchemyError as e:
            return BaseResponse[None](
                Status="Failed",
                Message=f"Database error: {str(e)}",
                Data=None
            )
        except Exception as e:
            return BaseResponse[None](
                Status="Failed",
                Message=f"Unexpected error: {str(e)}",
                Data=None
            )
    


    async def get_student_details(self, db: Session, token: str):
        try:
            # Decode token
            try:
                payload = AuthHandler({"token": token}).decode_token()
            except ValueError as e:
                return BaseResponse[None](
                    Status="Failed",
                    Message=str(e),
                    Data=None
                )

            student_id = payload.get("sub")
            if not student_id:
                return BaseResponse[None](
                    Status="Failed",
                    Message="Invalid token: no student ID found",
                    Data=None
                )

            # Fetch student from DB
            student = db.query(StudentModel).filter(StudentModel.id == int(student_id)).first()
            if not student:
                return BaseResponse[None](
                    Status="Failed",
                    Message="Student not found",
                    Data=None
                )

            return BaseResponse[StudentGet](
                Status="Success",
                Message="Student details retrieved successfully",
                Data=StudentGet.from_orm(student)
            )

        except SQLAlchemyError as e:
            return BaseResponse[None](
                Status="Failed",
                Message=f"Database error: {str(e)}",
                Data=None
            )
        except Exception as e:
            return BaseResponse[None](
                Status="Failed",
                Message=f"Unexpected error: {str(e)}",
                Data=None
            )
    

    async def update_student(self, db: Session, token: str, student_data: dict):
        try:
            # Decode token to get student_id
            try:
                payload = AuthHandler({"token": token}).decode_token()
            except ValueError as e:
                return BaseResponse[None](
                    Status="Failed",
                    Message=str(e),
                    Data=None
                )

            student_id = payload.get("sub")
            if not student_id:
                return BaseResponse[None](
                    Status="Failed",
                    Message="Invalid token: no student ID found",
                    Data=None
                )

            # Fetch student from DB
            student = db.query(StudentModel).filter(StudentModel.id == int(student_id)).first()
            if not student:
                return BaseResponse[None](
                    Status="Failed",
                    Message="Student not found",
                    Data=None
                )

            # Update only provided fields
            for key, value in student_data.items():
                if key == "password":  # Special handling for password
                    hashed_password = AuthHandler({"password": value}).get_password_hash()
                    setattr(student, "hashed_password", hashed_password)
                elif hasattr(student, key):
                    setattr(student, key, value)

            db.commit()
            db.refresh(student)

            return BaseResponse[StudentGet](
                Status="Success",
                Message="Student updated successfully",
                Data=StudentGet.from_orm(student)
            )

        except SQLAlchemyError as e:
            db.rollback()
            return BaseResponse[None](
                Status="Failed",
                Message=f"Database error: {str(e)}",
                Data=None
            )
        except Exception as e:
            return BaseResponse[None](
                Status="Failed",
                Message=f"Unexpected error: {str(e)}",
                Data=None
            )
