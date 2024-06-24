from sqlalchemy.orm import Session
from app.models.user import Role, Permission, RolePermission
from app.schemas.user import RoleCreate, RoleUpdate


def get_role(db: Session, role_id: int):
    return db.query(Role).filter(Role.id == role_id).first()


def get_role_by_name(db: Session, name: str):
    return db.query(Role).filter(Role.name == name).first()


def get_roles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Role).offset(skip).limit(limit).all()


def create_role(db: Session, role: RoleCreate):
    db_role = Role(name=role.name)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


def update_role(db: Session, role_id: int, role_update: RoleUpdate):
    db_role = get_role(db, role_id)
    if db_role:
        update_data = role_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            if key == "permissions":
                db_role.permissions = []
                for perm_name in value:
                    perm = db.query(Permission).filter(Permission.name == perm_name).first()
                    if perm:
                        db_role.permissions.append(perm)
            else:
                setattr(db_role, key, value)
        db.commit()
        db.refresh(db_role)
    return db_role


def delete_role(db: Session, role_id: int):
    db_role = get_role(db, role_id)
    if db_role:
        db.delete(db_role)
        db.commit()
    return db_role
