from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str | None
    description: str | None
    price: int | None
    discount: int | None
    img: str | None

    class Config:
        orm_mode = True
        use_enum_values = True
