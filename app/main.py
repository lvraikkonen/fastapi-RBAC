from fastapi import FastAPI
from app.api.v1.endpoints import user, role, permission, post
from app.db.database import engine, SessionLocal
from app.models import user as user_models, post as post_models
from app.models.user import Role
from app.scripts.init_db import init_db, init_sample_data


user_models.Base.metadata.create_all(bind=engine)
post_models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# 创建默认角色
def create_default_roles():
    db = SessionLocal()
    default_roles = ["admin", "user"]
    for role_name in default_roles:
        existing_role = db.query(Role).filter(Role.name == role_name).first()
        if not existing_role:
            new_role = Role(name=role_name)
            db.add(new_role)
    db.commit()
    db.close()


@app.on_event("startup")
async def startup_event():
    create_default_roles()
    init_db()
    init_sample_data()

app.include_router(user.router, prefix="/api/v1")
app.include_router(role.router, prefix="/api/v1")
app.include_router(permission.router, prefix="/api/v1")
app.include_router(post.router, prefix="/api/v1")


@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}
