from fastapi import Depends, HTTPException, status
from app.services.auth import get_current_user
from app.models.user import User


def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_admin_user(current_user: User = Depends(get_current_active_user)):
    if "admin" not in [role.name for role in current_user.roles]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    return current_user


def check_permission(required_permission: str):
    def permission_checker(current_user: User = Depends(get_current_user)):
        for role in current_user.roles:
            for permission in role.permissions:
                if permission.name == required_permission:
                    return current_user
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have the required permission"
        )
    return permission_checker
