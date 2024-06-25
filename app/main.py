from fastapi import FastAPI
import asyncio
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import user, role, permission, post
from app.scripts.init_db import init_db, init_sample_data
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan_context(app: FastAPI):
    # 在应用启动时同步初始化数据库
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, init_db)
    await loop.run_in_executor(None, init_sample_data)
    yield
    # 在应用关闭时执行清理操作（如果需要）


# 创建 FastAPI 实例
app = FastAPI(title="Basic FastAPI-RBAC Project", version="1.0.0", lifespan=lifespan_context)

# 配置 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 可以根据需要设置允许的源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user.router, prefix="/api/v1", tags=["users"])
app.include_router(role.router, prefix="/api/v1", tags=["roles"])
app.include_router(permission.router, prefix="/api/v1",tags=["permission"])
app.include_router(post.router, prefix="/api/v1", tags=["posts"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
