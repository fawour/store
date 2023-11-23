import sqlalchemy as sa
from db.base_class import Base


class User(Base):
    """ Пользователь """
    localized_name = 'Пользователь'

    id = sa.Column(sa.String, primary_key=True, index=True)
    firstname = sa.Column(sa.String)
    lastname = sa.Column(sa.String)
    admin = sa.Column(sa.Boolean, default=False)
    created = sa.Column(sa.DateTime(timezone=True), default=sa.func.now())

