from typing import Any

import inflection
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    id: Any
    __name__: str
    localized_name: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return inflection.underscore(cls.__name__)

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}: {self.id}>'
