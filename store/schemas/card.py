from pydantic import BaseModel


class CardBase(BaseModel):
    name: str
    price: int
