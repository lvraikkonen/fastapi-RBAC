from sqlalchemy.orm import Session
from app.models.user import User
from app.models.user import Role, Permission, RolePermission
from app.db.database import engine, SessionLocal
from app.core.security import get_password_hash
from app.services import user_service
from app.schemas.user import UserCreate
from app.models import user as user_models, post as post_models


user_models.Base.metadata.create_all(bind=engine)
post_models.Base.metadata.create_all(bind=engine)


def init_db():
    db = SessionLocal()

    # 创建admin角色（如果不存在）
    admin_role = db.query(Role).filter(Role.name == "admin").first()
    if not admin_role:
        admin_role = Role(name="admin")
        db.add(admin_role)
        db.commit()

    # 创建一个管理员用户（如果不存在）
    admin_user = db.query(User).filter(User.email == "admin@example.com").first()
    if not admin_user:
        admin_user = User(
            email="admin@example.com",
            hashed_password=get_password_hash("123456"),
            is_active=True
        )
        admin_user.roles.append(admin_role)
        db.add(admin_user)
        db.commit()


def init_sample_data():
    db = SessionLocal()

    # 创建角色
    roles = ["Admin", "Manager", "Editor", "User"]
    db_roles = {}
    for role_name in roles:
        role = db.query(Role).filter(Role.name == role_name).first()
        if not role:
            role = Role(name=role_name)
            db.add(role)
            db.commit()
        db_roles[role_name] = role

    # 创建权限
    permissions = [
        "create_user", "delete_user", "edit_user", "view_user",
        "create_post", "delete_post", "edit_post", "view_post",
        "manage_roles"
    ]
    db_permissions = {}
    for perm_name in permissions:
        perm = db.query(Permission).filter(Permission.name == perm_name).first()
        if not perm:
            perm = Permission(name=perm_name)
            db.add(perm)
            db.commit()
        db_permissions[perm_name] = perm

    # 定义角色-权限关系
    role_permissions = {
        "Admin": permissions,
        "Manager": ["create_user", "edit_user", "view_user", "create_post", "delete_post", "edit_post", "view_post"],
        "Editor": ["view_user", "create_post", "edit_post", "view_post"],
        "User": ["view_user", "view_post"]
    }

    # 分配权限给角色
    for role_name, perms in role_permissions.items():
        role = db_roles[role_name]
        for perm_name in perms:
            perm = db_permissions[perm_name]
            role_perm = db.query(RolePermission).filter_by(role_id=role.id, permission_id=perm.id).first()
            if not role_perm:
                role_perm = RolePermission(role_id=role.id, permission_id=perm.id)
                db.add(role_perm)
        db.commit()

    # 创建样例用户
    sample_users = [
        {"email": "admin@example.com", "password": "adminpass", "role": "Admin"},
        {"email": "manager@example.com", "password": "managerpass", "role": "Manager"},
        {"email": "editor@example.com", "password": "editorpass", "role": "Editor"},
        {"email": "user@example.com", "password": "userpass", "role": "User"}
    ]

    for user_data in sample_users:
        existing_user = user_service.get_user_by_email(db, user_data["email"])
        if not existing_user:
            user = user_service.create_user(db, UserCreate(email=user_data["email"], password=user_data["password"]))
            role = db_roles[user_data["role"]]
            user.roles.append(role)
            db.commit()


if __name__ == "__main__":
    init_db()
    init_sample_data()
    print("Database initialized with admin user and roles.")
