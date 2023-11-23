from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from db.crud import crud_product
from schemas import product as schema

router = APIRouter()

templates = Jinja2Templates(directory="src/templates")


@router.get("/product")
def get_product(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})


@router.get("/products")
def get_product_list(request: Request):
    return templates.TemplateResponse("store.html", {"request": request, 'operations': crud_product.get_product().all()})


@router.post("/product-create")
def create_product(obj_in: schema.ProductBase):
    crud_product.create_product(obj_in=obj_in)
    return  
