from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas.user import User, Role as RoleSchema
from app.services import role_service
from app.utils.decorators import permission_required
from app.api.deps import get_current_active_user, get_current_user

router = APIRouter()


@router.get("/roles", response_model=List[RoleSchema])
@permission_required("view_roles")
def read_roles(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    roles = role_service.get_roles(db, skip=skip, limit=limit)
    return roles
