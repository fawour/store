from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.api_router import api_router
from core.config import settings
from core.middlewares import SQLAlchemyMiddleware

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="/api/swagger_doc.json",
    docs_url="/api/swagger",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    redoc_url=None,
    debug=settings.DEBUG
)

app.mount("/static", StaticFiles(directory="src/static"), name="static")


app.include_router(api_router)
app.add_middleware(SQLAlchemyMiddleware)
