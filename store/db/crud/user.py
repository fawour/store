from db.models import User
from .base import CRUDBase
from sqlalchemy.orm import Query
from db.session import session


class CRUDUser(CRUDBase):
    model: User

    def query(self) -> Query:
        return session.query(self.model)

    def get_users(self):
        return self.query()


crud_user = CRUDUser(User)
