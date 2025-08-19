from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.community_posts import (
    Community_Posts as CommunityPostModel,
    Community_Posts_Comments as CommunityPostCommentModel,
    Community_Posts_Likes as CommunityPostLikeModel,
)
from app.models.student import Student as StudentModel
from app.schemas.common import BaseResponse
from app.routers.auth import AuthHandler
from app.schemas.community_posts import (GetCommunityPost)


class CommunityPostsHandler:

    async def create_post(self, db: Session, token: str, post_data: dict):
        try:
            # Decode token -> student_id
            try:
                payload = AuthHandler({"token": token}).decode_token()
            except ValueError as e:
                return BaseResponse[None](Status="Failed", Message=str(e), Data=None)

            student_id = payload.get("sub")
            if not student_id:
                return BaseResponse[None](
                    Status="Failed", Message="Invalid token: no student ID found", Data=None
                )

            # Ensure student exists
            student = db.query(StudentModel).filter(StudentModel.id == int(student_id)).first()
            if not student:
                return BaseResponse[None](
                    Status="Failed", Message="Student not found", Data=None
                )

            # Create post
            new_post = CommunityPostModel(student_id=int(student_id), **post_data)
            db.add(new_post)
            db.commit()
            db.refresh(new_post)

            return BaseResponse[dict](
                Status="Success",
                Message="Post created successfully",
                Data={"post_id": new_post.id, "title": new_post.post_title},
            )

        except SQLAlchemyError as e:
            db.rollback()
            return BaseResponse[None](
                Status="Failed", Message=f"Database error: {str(e)}", Data=None
            )
        except Exception as e:
            return BaseResponse[None](
                Status="Failed", Message=f"Unexpected error: {str(e)}", Data=None
            )

    async def add_comment(self, db: Session, token: str, comment_data: dict):
        try:
            # Decode token -> student_id
            try:
                payload = AuthHandler({"token": token}).decode_token()
            except ValueError as e:
                return BaseResponse[None](Status="Failed", Message=str(e), Data=None)

            student_id = payload.get("sub")
            if not student_id:
                return BaseResponse[None](
                    Status="Failed", Message="Invalid token: no student ID found", Data=None
                )

            # Ensure post exists
            post = db.query(CommunityPostModel).filter(
                CommunityPostModel.id == comment_data.get("post_id")
            ).first()
            if not post:
                return BaseResponse[None](
                    Status="Failed", Message="Post not found", Data=None
                )

            # Create comment
            new_comment = CommunityPostCommentModel(
                
                student_id=int(student_id),
                **comment_data,
            )
            db.add(new_comment)
            db.commit()
            db.refresh(new_comment)

            return BaseResponse[dict](
                Status="Success",
                Message="Comment added successfully",
                Data={"comment_id": new_comment.id, "comment": new_comment.comment},
            )

        except SQLAlchemyError as e:
            db.rollback()
            return BaseResponse[None](
                Status="Failed", Message=f"Database error: {str(e)}", Data=None
            )
        except Exception as e:
            return BaseResponse[None](
                Status="Failed", Message=f"Unexpected error: {str(e)}", Data=None
            )

    async def add_reaction(self, db: Session, token: str, reaction_data: dict):
        try:
            # Decode token -> student_id
            try:
                payload = AuthHandler({"token": token}).decode_token()
            except ValueError as e:
                return BaseResponse[None](Status="Failed", Message=str(e), Data=None)

            student_id = payload.get("sub")
            if not student_id:
                return BaseResponse[None](
                    Status="Failed", Message="Invalid token: no student ID found", Data=None
                )

            # Ensure post exists
            post = db.query(CommunityPostModel).filter(
                CommunityPostModel.id == reaction_data.get("post_id")
            ).first()
            if not post:
                return BaseResponse[None](
                    Status="Failed", Message="Post not found", Data=None
                )

            # Check if already liked (to avoid duplicates)
            existing_like = db.query(CommunityPostLikeModel).filter(
                CommunityPostLikeModel.post_id == post.id,
                CommunityPostLikeModel.student_id == int(student_id),
            ).first()

            if existing_like:
                return BaseResponse[None](
                    Status="Failed", Message="You already liked this post", Data=None
                )

            # Add like
            new_like = CommunityPostLikeModel(
                post_id=post.id,
                student_id=int(student_id),
            )
            db.add(new_like)
            db.commit()
            db.refresh(new_like)

            return BaseResponse[dict](
                Status="Success",
                Message="Reaction added successfully",
                Data={"like_id": new_like.id, "post_id": post.id},
            )

        except SQLAlchemyError as e:
            db.rollback()
            return BaseResponse[None](
                Status="Failed", Message=f"Database error: {str(e)}", Data=None
            )
        except Exception as e:
            return BaseResponse[None](
                Status="Failed", Message=f"Unexpected error: {str(e)}", Data=None
            )

    async def get_posts(self, db: Session, token: str):
        try:
            # Decode token (validation only)
            try:
                AuthHandler({"token": token}).decode_token()
            except ValueError as e:
                return BaseResponse[None](Status="Failed", Message=str(e), Data=None)

            # Fetch latest 10 posts
            posts = (
                db.query(CommunityPostModel)
                .order_by(CommunityPostModel.post_date.desc())
                .limit(10)
                .all()
            )

            if not posts:
                return BaseResponse[list[GetCommunityPost]](
                    Status="Success", Message="No posts available", Data=[]
                )

            # Convert to schema format
            result = []
            for post in posts:
                result.append(
                    GetCommunityPost(
                        id=post.id,
                        student_id=post.student_id,
                        post_title=post.post_title,
                        post_content=post.post_content,
                        post_date=post.post_date,
                        likes_count=len(post.likes),
                        comments_count=len(post.comments),
                    )
                )

            return BaseResponse[list[GetCommunityPost]](
                Status="Success",
                Message="Posts retrieved successfully",
                Data=result,
            )

        except SQLAlchemyError as e:
            return BaseResponse[None](
                Status="Failed", Message=f"Database error: {str(e)}", Data=None
            )
        except Exception as e:
            return BaseResponse[None](
                Status="Failed", Message=f"Unexpected error: {str(e)}", Data=None
            )
