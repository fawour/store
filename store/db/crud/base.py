import contextlib
from typing import Any, Dict, Generic, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from psycopg2.errors import UniqueViolation
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Query

from db.base_class import Base
from db.session import session

ModelType = TypeVar("ModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType]):
    order_columns = None
    filter_columns = None
    search_columns: list = []

    @property
    def search_query_param(self) -> str:
        return "search"

    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        """
        self.model = model

    def get(self, id: Any) -> ModelType | None:
        return session.query(self.model).get(id)

    def query(self) -> Query:
        return session.query(self.model)

    def _create(self, *, obj_in: SchemaType) -> ModelType:
        obj = self.create(obj_in=obj_in)
        self.commit_obj(obj)
        return obj

    def create(self, *, obj_in: SchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        return db_obj

    def update(
        self,
        *,
        db_obj: ModelType,
        obj_in: Union[SchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        return db_obj

    def _update(
        self,
        *,
        db_obj: ModelType,
        obj_in: Union[SchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj = self.update(db_obj=db_obj, obj_in=obj_in)
        self.commit_obj(obj)
        return obj

    def commit_obj(self, db_obj) -> None:
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)

    def rollback(self) -> None:
        session.rollback()

    def _remove(self, *, db_obj: ModelType) -> ModelType:
        session.delete(db_obj)
        session.commit()
        return db_obj

    @contextlib.contextmanager
    def handle_duplicate(self, exc: Exception):
        try:
            yield
        except IntegrityError as e:
            self.rollback()
            if isinstance(e.orig, UniqueViolation):
                raise exc
            else:
                raise
