from sqlalchemy.orm import Session
from app.models.post import Post
from app.schemas.post import PostCreate


def create_post(db: Session, post: PostCreate, user_id: int):
    db_post = Post(**post.dict(), author_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Post).offset(skip).limit(limit).all()


def get_post(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()
