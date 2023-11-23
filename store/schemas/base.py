from typing import Optional
from fastapi import Query

from pydantic import BaseModel


class ResponseBase(BaseModel):
    request_id: Optional[str]


class PaginationParams(BaseModel):
    page: int = Query(1, ge=1, description="Page number")
    per_page: int = Query(100, ge=1, le=200, description="Page size")


class PaginatedMeta(PaginationParams):
    total_count: int


class PaginatedBase(BaseModel):
    meta: PaginatedMeta
    list: list
