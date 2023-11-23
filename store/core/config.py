import os
from typing import Any, List, Optional, Union
from uuid import uuid4

from dotenv import load_dotenv
from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, RedisDsn, validator

load_dotenv()


class Settings(BaseSettings):
    DEBUG: bool = bool(int(os.environ.get('DEBUG', 0)))

    PROJECT_NAME: str = 'Stor'
    APP_NAME: str = 'Stor'
    ADMIN_API_V1_STR: str = "/admin/api/v1"
    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:3000",
        "http://localhost",
        "http://127.0.0.1",
        "http://127.0.0.1:3000",
    ]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: Optional[str]
    POSTGRES_DB: str
    DATABASE_URL: Optional[PostgresDsn] = None

    @validator("DATABASE_URL", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            port=values.get("POSTGRES_PORT", '5432'),
            path=f'/{values.get("POSTGRES_DB")}',
        )

    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_CHANNEL: Optional[str]
    REDIS_USER: Optional[str]
    REDIS_PASSWORD: Optional[str]
    REDIS_URL: Optional[RedisDsn] = None

    @validator("REDIS_URL", pre=True)
    def assemble_redis_url(cls, v: Optional[str], values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return RedisDsn.build(
            scheme="redis",
            user=values.get("REDIS_USER"),
            password=values.get("REDIS_PASSWORD"),
            host=values.get("REDIS_HOST"),
            port=values.get("REDIS_PORT", '6379'),
            path=f'/{values.get("REDIS_CHANNEL") or "0"}',
        )

    DEFAULT_TIMEZONE: str = 'Europe/Moscow'

    TEST_TOKEN: str = str(uuid4())

    SWAGGER_SHOW_INTERNAL_API: bool = True

    class Config:
        case_sensitive = True


settings = Settings()
