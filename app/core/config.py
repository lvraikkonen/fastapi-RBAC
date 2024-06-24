from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# get configs from .env
load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    POOL_SIZE: int = int(os.getenv("POOL_SIZE", 10))
    MAX_OVERFLOW: int = int(os.getenv("MAX_OVERFLOW", 20))
    POOL_TIMEOUT: int = int(os.getenv("POOL_TIMEOUT", 30))
    POOL_RECYCLE: int = int(os.getenv("POOL_RECYCLE", 1800))

    class Config:
        env_file = ".env"
        extra = "ignore"  # 或者 "forbid"，根据需求选择


class DevelopmentSettings(Settings):
    # 开发环境使用本地SQLite数据库
    DATABASE_URL: str = os.getenv("DEVELOPMENT_DATABASE_URI")
    SECRET_KEY: str = os.getenv("DEVELOPMENT_SECRET_KEY")


class TestingSettings(Settings):
    # 测试环境使用本地SQLite数据库
    DATABASE_URL: str = os.getenv("TESTING_DATABASE_URI")
    SECRET_KEY: str = os.getenv("TESTING_SECRET_KEY")


class ProductionSettings(Settings):
    # 生产环境从环境变量中获取数据库URI和秘钥
    DATABASE_URL: str = os.getenv("PROD_DATABASE_URL")
    SECRET_KEY: str = os.getenv("PROD_SECRET_KEY")


def get_settings() -> Settings:
    """
    根据环境变量 ENV 的值选择相应的配置类。
    - development: 使用 DevelopmentSettings
    - testing: 使用 TestingSettings
    - production: 使用 ProductionSettings
    """
    env = os.getenv("ENV", "development")
    if env == "production":
        return ProductionSettings()
    elif env == "testing":
        return TestingSettings()
    else:
        return DevelopmentSettings()


# 创建 settings 实例，用于在整个应用程序中访问配置项
settings = get_settings()
