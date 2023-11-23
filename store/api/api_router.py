from fastapi import APIRouter


from api.api_v1 import (user, product, card)
from core.config import settings

api_router = APIRouter()

api_router.include_router(user.router, prefix=settings.API_V1_STR, tags=["User"])
api_router.include_router(product.router, prefix=settings.API_V1_STR, tags=["Product"])
api_router.include_router(card.router, prefix=settings.API_V1_STR, tags=["Card"])