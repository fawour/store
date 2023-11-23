from db.models import Product
from .base import CRUDBase
from sqlalchemy.orm import Query
from db.session import session
from schemas import product as schema

class CRUDProduct(CRUDBase):
    model: Product

    def query(self) -> Query:
        return session.query(self.model)

    def get_product(self):
        return self.query()

    def create_product(self, obj_in: schema.ProductBase):
        db_obj = self.model(**obj_in.dict())
        session.add(db_obj)
        session.commit()
        return db_obj


crud_product = CRUDProduct(Product)
