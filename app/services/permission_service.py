from sqlalchemy.orm import Session
from app.models.user import Permission
from app.schemas.user import PermissionCreate, PermissionUpdate
from fastapi import HTTPException


def get_permission(db: Session, permission_id: int):
    return db.query(Permission).filter(Permission.id == permission_id).first()


def get_permission_by_name(db: Session, name: str):
    return db.query(Permission).filter(Permission.name == name).first()


def get_permissions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Permission).offset(skip).limit(limit).all()


def create_permission(db: Session, permission: PermissionCreate):
    db_permission = Permission(name=permission.name)
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    return db_permission


def update_permission(db: Session, permission_id: int, permission_update: PermissionUpdate):
    db_permission = get_permission(db, permission_id)
    if not db_permission:
        raise HTTPException(status_code=404, detail="Permission not found")

    db_permission.name = permission_update.name
    db.commit()
    db.refresh(db_permission)
    return db_permission


def delete_permission(db: Session, permission_id: int):
    db_permission = get_permission(db, permission_id)
    if not db_permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    db.delete(db_permission)
    db.commit()
    return db_permission
