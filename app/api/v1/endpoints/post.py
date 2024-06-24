from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas.post import Post, PostCreate
from app.services import post_service
from app.services.auth import get_current_user
from app.utils.decorators import permission_required
from app.schemas.user import User

router = APIRouter()


@router.post("/posts/", response_model=Post)
@permission_required("create_post")
async def create_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return post_service.create_post(db=db, post=post, user_id=current_user.id)


@router.get("/posts/", response_model=List[Post])
@permission_required("view_post")
async def read_posts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    posts = post_service.get_posts(db, skip=skip, limit=limit)
    return posts


@router.get("/posts/{post_id}", response_model=Post)
@permission_required("view_post")
async def read_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    post = post_service.get_post(db, post_id=post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post
