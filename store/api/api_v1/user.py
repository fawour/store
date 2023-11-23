from fastapi import APIRouter, Depends
from db.crud import crud_user
from api import paginate
from schemas.base import PaginationParams

router = APIRouter()


@router.get("/user")
def get_user(params: PaginationParams = Depends()):
    return paginate(crud_user.get_users(), params)
