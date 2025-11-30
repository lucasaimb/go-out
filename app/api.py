# app/api.py
from fastapi import APIRouter

from app.modules.usuario.api import router as usuarios_router

router = APIRouter()

router.include_router(
    usuarios_router,
    prefix="/usuario",
    tags=["Usuários"],
)
