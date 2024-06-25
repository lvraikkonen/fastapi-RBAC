from sqlalchemy.orm import Session
from app.models.user import Role, Permission, RolePermission
from app.schemas.user import RoleCreate, RoleUpdate
from fastapi import HTTPException


def get_role(db: Session, role_id: int):
    return db.query(Role).filter(Role.id == role_id).first()


def get_roles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Role).offset(skip).limit(limit).all()


def get_role_by_name(db: Session, name: str):
    return db.query(Role).filter(Role.name == name).first()


def create_role(db: Session, role: RoleCreate):
    permissions = db.query(Permission).filter(Permission.name.in_(role.permissions)).all()
    db_role = Role(name=role.name, permissions=permissions)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


def update_role(db: Session, role_id: int, role_update: RoleUpdate):
    db_role = get_role(db, role_id)
    if not db_role:
        raise HTTPException(status_code=404, detail="Role not found")

    if role_update.name:
        db_role.name = role_update.name

    if role_update.permissions is not None:
        permissions = db.query(Permission).filter(Permission.name.in_(role_update.permissions)).all()
        db_role.permissions = permissions

    db.commit()
    db.refresh(db_role)
    return db_role


def delete_role(db: Session, role_id: int):
    db_role = get_role(db, role_id)
    if not db_role:
        raise HTTPException(status_code=404, detail="Role not found")
    db.delete(db_role)
    db.commit()
    return db_role
