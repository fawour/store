
from enum import Enum
from typing import Type

from pydantic import BaseModel
from sqlalchemy import or_, and_
from sqlalchemy.orm import Query

_orm_operator_transformer = {
    "neq": lambda value: ("__ne__", value),
    "gt": lambda value: ("__gt__", value),
    "gte": lambda value: ("__ge__", value),
    "in": lambda value: ("in_", value.split(',')),
    "isnull": lambda value: ("is_", None) if value is True else ("is_not", None),
    "lt": lambda value: ("__lt__", value),
    "lte": lambda value: ("__le__", value),
    "like": lambda value: ("like", f"%{value}%"),
    "ilike": lambda value: ("ilike", f"%{value}%"),
    "not": lambda value: ("is_not", value),
    "not_in": lambda value: ("not_in", value),
}


class FilterColumns:
    def __init__(self, columns: dict):
        for field_name, field in columns.items():
            setattr(self, field_name, field)


class SortColumns(FilterColumns):
    @property
    def fields_list(self) -> list:
        return [key for key in self.__dict__.keys() if not key.startswith('__')]

    @property
    def fields_descr(self) -> list:
        return 'Order columns: ' + ', '.join(self.fields_list)


class BaseFilter(BaseModel):
    class Constants:
        ordering_query_param: str = "ordering"
        search_query_param: str = "search"
        operators_param: str = "operators"

    class Meta:
        model: Type = None
        sort_columns: SortColumns = None
        filter_columns: FilterColumns = None
        search_columns: list = []

    @property
    def ordering_values(self) -> list[str]:
        try:
            return getattr(self, self.Constants.ordering_query_param).split(",")
        except AttributeError:
            return None

    @property
    def operators_values(self) -> list[str]:
        try:
            return getattr(self, self.Constants.operators_param).split(',')
        except AttributeError:
            return []

    @property
    def filtering_fields(self):
        exclude = {
            self.Constants.operators_param,
            self.Constants.ordering_query_param
        }
        fields = self.dict(exclude_none=True, exclude_unset=True, exclude=exclude)
        return fields.items()

    class OrderDirection(str, Enum):
        asc = "asc"
        desc = "desc"

    class Operators(str, Enum):
        and_ = "and"
        or_ = "or"

    def apply(self, query: Query) -> Query:
        query = self.filter(query)
        query = self.sort(query)
        return query

    def sort(self, query: Query) -> Query:
        if not self.ordering_values:
            return query

        for field_name in self.ordering_values:
            if not field_name:
                continue

            direction = self.OrderDirection.asc
            if field_name.startswith("-"):
                direction = self.OrderDirection.desc

            field_name = field_name.replace("-", "").replace("+", "")
            try:
                column = getattr(self.Meta.sort_columns, field_name)
            except AttributeError:
                continue

            query = query.order_by(getattr(column, direction)())

        return query

    def filter(self, query: Query) -> Query:
        _filters = []
        for _filter, value in self.filtering_fields:
            if "__" in _filter:
                field_name, operator = _filter.split("__")
                operator, value = _orm_operator_transformer[operator](value)
            else:
                field_name, operator = _filter, "__eq__"

            if field_name == self.Constants.search_query_param and self.Meta.search_columns:
                """ search in text columns """
                def search_filter(field):
                    return field.ilike("%" + value + "%")

                query = query.filter(or_(*list(map(search_filter, self.Meta.search_columns))))
            else:
                filter_columns = getattr(self.Meta, 'filter_columns', None) or self.Meta.model
                try:
                    column = getattr(filter_columns, field_name)
                except AttributeError:
                    continue

                _filters.append(getattr(column, operator)(value))

        operators = self.operators_values
        if operators:
            groupped_filters = tuple()
            group = []
            for _filter in _filters:
                try:
                    op = operators.pop(0)
                except IndexError:
                    op = self.Operators.and_

                group.append(_filter)
                if op == self.Operators.or_:
                    groupped_filters += (tuple(group), )
                    group.clear()

            groupped_filters += (tuple(group), )
            query = query.filter(or_(*[and_(*group) for group in groupped_filters]))
        else:
            query = query.filter(*_filters)

        return query
