from sqlalchemy.orm import Session
from app.models.user import User, Role, Permission
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password
from typing import List
from fastapi import HTTPException


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 10):
    """
    获取用户列表
    :param db: 数据库会话
    :param skip: 跳过的记录数
    :param limit: 返回的记录数
    :return: 用户列表
    """
    return db.query(User).offset(skip).limit(limit).all()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_user_by_name(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)

    # 获取默认的普通用户角色
    default_role = db.query(Role).filter(Role.name == "User").first()
    if not default_role:
        # 如果默认角色不存在，创建它
        default_role = Role(name="User")
        db.add(default_role)
        db.commit()

    db_user.roles.append(default_role)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, username: str, password: str):
    # user = get_user_by_email(db, email)
    user = get_user_by_name(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def update_user(db: Session, user_id: int, user_update: UserUpdate):
    db_user = get_user(db, user_id)
    if db_user:
        update_data = user_update.dict(exclude_unset=True)
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
        for key, value in update_data.items():
            if key == "roles":
                db_user.roles = []
                for role_name in value:
                    role = db.query(Role).filter(Role.name == role_name).first()
                    if role:
                        db_user.roles.append(role)
            else:
                setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user


def update_user_roles(db: Session, user_id: int, role_names: List[str]):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    roles = db.query(Role).filter(Role.name.in_(role_names)).all()
    user.roles = roles
    db.commit()
    db.refresh(user)
    return user
