from sqlalchemy.orm import Query

from schemas.base import PaginatedBase, PaginatedMeta, PaginationParams


def paginate(query: Query, params: PaginationParams) -> PaginatedBase:
    page = params.page
    per_page = params.per_page

    results = query.limit(per_page).offset((page - 1) * per_page).all()
    total_count = query.distinct().count()
    return PaginatedBase(
        meta=PaginatedMeta(page=page, per_page=per_page, total_count=total_count),
        list=results
    )
