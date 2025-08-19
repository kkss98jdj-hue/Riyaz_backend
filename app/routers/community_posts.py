from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from typing import Optional
from app.schemas.community_posts import (
    CommunityPostCreate,
    CommunityPostReactions,
    AddCommunityPostComment,
    GetCommunityPost,
)
from app.schemas.common import BaseResponse
from app.database import get_db
from app.crud.community_posts import CommunityPostsHandler

router = APIRouter()
community_posts_handler = CommunityPostsHandler()


@router.post("/createpost")
async def create_post(
    post: CommunityPostCreate,
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(None),
):
    if not authorization or not authorization.startswith("Bearer "):
        return BaseResponse[None](
            Status="Failed", Message="Invalid or missing token", Data=None
        )
    token = authorization.split(" ")[1]
    return await community_posts_handler.create_post(
        db=db, token=token, post_data=post.dict()
    )


@router.post("/addcomment")
async def add_comment(
    comment: AddCommunityPostComment,
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(None),
):
    if not authorization or not authorization.startswith("Bearer "):
        return BaseResponse[None](
            Status="Failed", Message="Invalid or missing token", Data=None
        )
    token = authorization.split(" ")[1]
    return await community_posts_handler.add_comment(
        db=db, token=token, comment_data=comment.dict()
    )


@router.post("/addreaction")
async def add_reaction(
    reaction: CommunityPostReactions,
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(None),
):
    if not authorization or not authorization.startswith("Bearer "):
        return BaseResponse[None](
            Status="Failed", Message="Invalid or missing token", Data=None
        )
    token = authorization.split(" ")[1]
    return await community_posts_handler.add_reaction(
        db=db, token=token, reaction_data=reaction.dict()
    )


@router.get("/getposts")
async def get_posts(
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(None),
):
    if not authorization or not authorization.startswith("Bearer "):
        return BaseResponse[None](
            Status="Failed", Message="Invalid or missing token", Data=None
        )
    token = authorization.split(" ")[1]
    return await community_posts_handler.get_posts(
        db=db, token=token
    )
