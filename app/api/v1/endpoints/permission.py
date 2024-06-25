from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas.user import User, Permission as PermissionSchema
from app.services import permission_service
from app.utils.decorators import permission_required
from app.api.deps import get_current_active_user, get_current_user

router = APIRouter()


@router.get("/permissions", response_model=List[PermissionSchema])
@permission_required("view_permissions")
def read_permissions(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    permissions = permission_service.get_permissions(db, skip=skip, limit=limit)
    return permissions
