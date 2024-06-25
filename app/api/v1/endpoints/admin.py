from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.models.user import User
from app.schemas.user import User as UserSchema, Role as RoleSchema, Permission as PermissionSchema
from app.schemas.user import RoleCreate, RoleUpdate, PermissionCreate, PermissionUpdate
from app.api.deps import get_current_user
from app.utils.decorators import permission_required
from app.services import user_service, role_service, permission_service


router = APIRouter()


# 用户管理
@router.get("/users", response_model=List[UserSchema])
@permission_required("manage_users")
async def get_all_users(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    users = user_service.get_users(db, skip=skip, limit=limit)
    return users


# 更新用户role
@router.put("/users/{user_id}/roles", response_model=UserSchema)
@permission_required("manage_users")
async def update_user_roles(
    user_id: int,
    role_names: List[str],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return user_service.update_user_roles(db, user_id, role_names)


# 角色管理
@router.post("/roles", response_model=RoleSchema)
@permission_required("manage_roles")
async def create_role(
    role: RoleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return role_service.create_role(db, role)


@router.get("/roles", response_model=List[RoleSchema])
@permission_required("manage_roles")
async def get_all_roles(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    roles = role_service.get_roles(db, skip=skip, limit=limit)
    return roles


@router.put("/roles/{role_id}", response_model=RoleSchema)
@permission_required("manage_roles")
async def update_role(
    role_id: int,
    role_update: RoleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return role_service.update_role(db, role_id, role_update)


@router.delete("/roles/{role_id}", response_model=RoleSchema)
@permission_required("manage_roles")
async def delete_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return role_service.delete_role(db, role_id)


# 权限管理
@router.post("/permissions", response_model=PermissionSchema)
@permission_required("manage_permissions")
async def create_permission(
    permission: PermissionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return permission_service.create_permission(db, permission)


@router.get("/permissions", response_model=List[PermissionSchema])
@permission_required("manage_permissions")
async def get_all_permissions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    permissions = permission_service.get_permissions(db, skip=skip, limit=limit)
    return permissions


@router.put("/permissions/{permission_id}", response_model=PermissionSchema)
@permission_required("manage_permissions")
async def update_permission(
    permission_id: int,
    permission_update: PermissionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return permission_service.update_permission(db, permission_id, permission_update)


@router.delete("/permissions/{permission_id}", response_model=PermissionSchema)
@permission_required("manage_permissions")
async def delete_permission(
    permission_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return permission_service.delete_permission(db, permission_id)
