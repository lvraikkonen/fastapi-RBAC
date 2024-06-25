from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.core.security import create_access_token
from app.services import user_service
from app.schemas.user import User as UserSchema
from app.schemas.user import User, UserCreate, UserUpdate, Token
from app.api.deps import get_current_active_user, get_current_user
from app.utils.decorators import permission_required

router = APIRouter()


@router.post("/register", response_model=UserSchema)
@permission_required("create_user")
def create_user(user: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # 检查用户名是否已经存在
    existing_user = user_service.get_user_by_name(db, user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    # 检查邮箱是否已经存在
    existing_email = user_service.get_user_by_email(db, user.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    db_user = user_service.create_user(db, user)
    return db_user


@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = user_service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=User)
def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.put("/users/me", response_model=UserSchema)
def update_user_me(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user)
):
    return user_service.update_user(db, current_user.id, user_update)
