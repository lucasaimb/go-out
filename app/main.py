# app/main.py
from fastapi import FastAPI
from app.api import router as api_router


def create_app() -> FastAPI:
    app = FastAPI(title="GoOut API (MVP)")

    # registra rotas da aplicação (incluindo /usuario)
    app.include_router(api_router)

    return app


app = create_app()
