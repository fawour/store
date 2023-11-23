from sqlalchemy.orm import Query

from db.models import Card, Product
from db.session import session
from .base import CRUDBase


class CRUDCard(CRUDBase):
    model: Card

    def query(self) -> Query:
        return session.query(self.model)

    def get_card(self):
        return self.query()

    def create_card(self, product_id):
        b = session.query(Card).filter(Card.product_id == product_id).first()

        if not b:
            name = session.query(Product.name).filter(Product.id == product_id).first()
            price = session.query(Product.price).filter(Product.id == product_id).first()
            img = session.query(Product.img).filter(Product.id == product_id).first()
            db_obj = self.model(name=name[0], price=price[0], product_id=product_id,img=img[0], quantity=1)
            session.add(db_obj)
        else:
            quantity = session.query(Card.quantity).filter(Card.product_id == product_id).first()
            quantity = quantity[0] + 1
            price_old = session.query(Card.price).filter(Card.product_id == product_id).first()
            price_new = session.query(Product.price).filter(Product.id == product_id).first()
            price = price_old[0] + price_new[0]
            session.query(Card).filter(Card.product_id == product_id).update({'quantity': quantity, 'price': price})
        session.commit()

    def delete_card(self):
        session.query(Card).delete()
        session.commit()


crud_card = CRUDCard(Card)
