from pydantic import BaseModel, EmailStr
from typing import List, Optional


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class RoleBase(BaseModel):
    name: str

    class Config:
        orm_mode = True


class RoleCreate(RoleBase):
    pass


class Role(RoleBase):
    id: int
    permissions: List[str] = []

    class Config:
        orm_mode = True


class PermissionBase(BaseModel):
    name: str


class PermissionCreate(PermissionBase):
    pass


class Permission(PermissionBase):
    id: int

    class Config:
        orm_mode = True


class RoleUpdate(BaseModel):
    name: Optional[str] = None
    permissions: Optional[List[str]] = None


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    roles: List[RoleBase] = []

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    roles: Optional[List[str]] = None
