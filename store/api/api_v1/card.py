from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from db.crud import crud_card

router = APIRouter()

templates = Jinja2Templates(directory="src/templates")


@router.get("/card")
def get_my_card(request: Request):
    return templates.TemplateResponse("card.html", {"request": request, 'operations': crud_card.get_card().all()})


@router.post("/card_add/{product_id}")
def create_card(product_id: int):
    crud_card.create_card(product_id)


@router.delete("/card_delete")
def delete_card():
    crud_card.delete_card()
