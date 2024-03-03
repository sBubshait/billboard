from __future__ import annotations

from databases import DatabaseURL
from fastapi import FastAPI
from fastapi import Request

from trading.api import rest
from trading import settings
from trading.adapters.mysql import MySQLService

import urllib.parse

def init_mysql(app: FastAPI) -> None:
    database_url = DatabaseURL(
        "mysql+asyncmy://{username}:{password}@{host}:{port}/{db}".format(
            username=settings.MYSQL_USER,
            password=urllib.parse.quote(settings.MYSQL_PASSWORD),
            host=settings.MYSQL_HOST,
            port=settings.MYSQL_PORT,
            db=settings.MYSQL_DB,
        ),
    )

    app.state.mysql = MySQLService(database_url)

    @app.on_event("startup")
    async def on_startup() -> None:
        await app.state.mysql.connect()

    @app.on_event("shutdown")
    async def on_shutdown() -> None:
        await app.state.mysql.disconnect()

    # Context based transactions.
    @app.middleware("http")
    async def mysql_transaction(request: Request, call_next):
        async with app.state.mysql.transaction() as sql:
            request.state.mysql = sql
            return await call_next(request)

def configure_routers(app: FastAPI) -> None:
    app.include_router(rest.router)


def create_app() -> FastAPI:
    app = FastAPI()
    configure_routers(app)
    init_mysql(app)
    return app



asgi_app = create_app()
