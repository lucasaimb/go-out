from sqlalchemy import create_engine
from app.core.config import settings
from sqlalchemy.engine import Connection
from contextlib import contextmanager

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

@contextmanager
def get_connection() -> Connection:
    """
    Abre uma conexão dentro de uma transação.
    A transação é comitada automaticamente ao final.
    """
    with engine.begin() as conn:
        yield conn
