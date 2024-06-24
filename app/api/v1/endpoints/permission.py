from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas.user import Permission, PermissionCreate
from app.services import permission_service

router = APIRouter()


@router.post("/permissions/", response_model=Permission)
def create_permission(permission: PermissionCreate, db: Session = Depends(get_db)):
    db_permission = permission_service.get_permission_by_name(db, name=permission.name)
    if db_permission:
        raise HTTPException(status_code=400, detail="Permission already exists")
    return permission_service.create_permission(db=db, permission=permission)


@router.get("/permissions/", response_model=List[Permission])
def read_permissions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    permissions = permission_service.get_permissions(db, skip=skip, limit=limit)
    return permissions


@router.get("/permissions/{permission_id}", response_model=Permission)
def read_permission(permission_id: int, db: Session = Depends(get_db)):
    db_permission = permission_service.get_permission(db, permission_id=permission_id)
    if db_permission is None:
        raise HTTPException(status_code=404, detail="Permission not found")
    return db_permission


@router.delete("/permissions/{permission_id}", response_model=Permission)
def delete_permission(permission_id: int, db: Session = Depends(get_db)):
    db_permission = permission_service.delete_permission(db, permission_id=permission_id)
    if db_permission is None:
        raise HTTPException(status_code=404, detail="Permission not found")
    return db_permission
