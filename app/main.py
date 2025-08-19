from fastapi import FastAPI

from app.database import Base,engine

from app.models.student import Student as StudentModel

from app.schemas.common import BaseResponse

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.routers.student import router as student_router

from app.routers.community_posts import router as community_posts_router


app=FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content=BaseResponse[None](
            Status="Failed",
            Message="Request Validation error",
            Data=str(exc.errors())
        ).dict()
    )



@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)



app.include_router(student_router,tags=["student"])
app.include_router(community_posts_router,tags=["community_posts"])