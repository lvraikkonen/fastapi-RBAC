from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas.user import Role, RoleCreate, RoleUpdate
from app.services import role_service

router = APIRouter()


@router.post("/roles/", response_model=Role)
def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    db_role = role_service.get_role_by_name(db, name=role.name)
    if db_role:
        raise HTTPException(status_code=400, detail="Role already exists")
    return role_service.create_role(db=db, role=role)


@router.get("/roles/", response_model=List[Role])
def read_roles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    roles = role_service.get_roles(db, skip=skip, limit=limit)
    return roles


@router.get("/roles/{role_id}", response_model=Role)
def read_role(role_id: int, db: Session = Depends(get_db)):
    db_role = role_service.get_role(db, role_id=role_id)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return db_role


@router.put("/roles/{role_id}", response_model=Role)
def update_role(role_id: int, role: RoleUpdate, db: Session = Depends(get_db)):
    db_role = role_service.update_role(db, role_id=role_id, role_update=role)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return db_role


@router.delete("/roles/{role_id}", response_model=Role)
def delete_role(role_id: int, db: Session = Depends(get_db)):
    db_role = role_service.delete_role(db, role_id=role_id)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return db_role
