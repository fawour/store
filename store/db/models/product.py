import sqlalchemy as sa
from db.base_class import Base


class Product(Base):
    """ Товары """
    localized_name = 'Товары'

    id = sa.Column(sa.BigInteger, primary_key=True, index=True)
    name = sa.Column(sa.String)
    description = sa.Column(sa.String)
    price = sa.Column(sa.Integer)
    discount = sa.Column(sa.Integer)
    created = sa.Column(sa.DateTime(timezone=True), default=sa.func.now())
    img = sa.Column(sa.String)
