from functools import wraps
from fastapi import HTTPException, Depends, status
from app.services.auth import get_current_user
from app.models.user import User
import inspect


def permission_required(required_permission: str):
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            current_user: User = kwargs.get('current_user')
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not authenticated"
                )

            for role in current_user.roles:
                for permission in role.permissions:
                    if permission.name == required_permission:
                        return await func(*args, **kwargs)

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="The user doesn't have the required permission"
            )

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            current_user: User = kwargs.get('current_user')
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not authenticated"
                )

            for role in current_user.roles:
                for permission in role.permissions:
                    if permission.name == required_permission:
                        return func(*args, **kwargs)

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="The user doesn't have the required permission"
            )

        if inspect.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper

    return decorator
