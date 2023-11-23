import sqlalchemy as sa
from db.base_class import Base


class Card(Base):
    """ Корзина """
    localized_name = 'Корзина'

    id = sa.Column(sa.BigInteger, primary_key=True, index=True)
    name = sa.Column(sa.String)
    price = sa.Column(sa.Integer)
    product_id = sa.Column(sa.Integer)
    quantity = sa.Column(sa.Integer)
    img = sa.Column(sa.String)

