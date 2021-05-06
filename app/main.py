from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.exceptions import RequestValidationError

from app.domain.config import *
from app.domain.constants import *
from app.controllers.user_controller import controller as user_controller
from app.controllers.game_controller import controller as game_controller
from app.data.migrations_manager import migrate_database
from app.exceptions.app_exceptions import AppDomainException
from app.exceptions.handlers import exception_handler, app_exception_handler, validation_exception_handler
from app.logger.custom_logger import logger


app = FastAPI(
    title="Amber API",
    version="1.0",
    openapi_url=OPEN_API_URL,
    docs_url=DOCS_URL
)


migrate_database(MIGRATIONS_DIR, ALEMBIC_INI_DIR, SQLALCHEMY_DATABASE_URL)


@app.exception_handler(RequestValidationError)
async def custom_validation_exception_handler(request, e):
    return await validation_exception_handler(request, e)


@app.exception_handler(AppDomainException)
async def custom_app_exception_handler(request, e):
    return await app_exception_handler(request, e)


@app.exception_handler(Exception)
async def custom_app_exception_handler(request, e):
    return await exception_handler(request, e)


app.include_router(user_controller)
app.include_router(game_controller)


@app.get("/", include_in_schema=False)
async def index():
    response = RedirectResponse(url=DOCS_URL)
    logger.info(f"Redirecting to swagger docs; {DOCS_URL}")

    return response
