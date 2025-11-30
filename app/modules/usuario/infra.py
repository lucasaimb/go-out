# app/modules/usuario/infra.py
from typing import List, Optional

from sqlalchemy import text

from app.core.db import get_connection
from app.modules.usuario.domain import Usuario, UsuarioRepository


class SqlAlchemyUsuarioRepository(UsuarioRepository):
    """Implementação de UsuarioRepository usando SQLAlchemy + Supabase."""

    def listar(self) -> List[Usuario]:
        """Retorna todos os usuários da tabela 'Usuario'."""
        with get_connection() as conn:
            result = conn.execute(text('SELECT * FROM "Usuario"'))
            rows = result.fetchall()
            return [self._row_to_usuario(row) for row in rows]

    def buscar_por_id(self, usuario_id: int) -> Optional[Usuario]:
        """Retorna um usuário pelo ID, ou None se não existir."""
        with get_connection() as conn:
            result = conn.execute(
                text('SELECT * FROM "Usuario" WHERE id = :id'),
                {"id": usuario_id},
            )
            row = result.fetchone()
            return self._row_to_usuario(row) if row else None

    def criar(
        self,
        nome: str,
        email: str,
        senha_hash: str,
        tipo_conta: str = "usuario",
    ) -> Usuario:
        """
        Cria um novo usuário na tabela 'Usuario' e retorna um objeto de domínio.
        """
        query = text("""
            INSERT INTO "Usuario" (nome, email, senha_hash, data_cadastro, tipo_conta)
            VALUES (:nome, :email, :senha_hash, CURRENT_DATE, :tipo_conta)
            RETURNING *;
        """)

        with get_connection() as conn:
            result = conn.execute(
                query,
                {
                    "nome": nome,
                    "email": email,
                    "senha_hash": senha_hash,
                    "tipo_conta": tipo_conta,
                },
            )
            row = result.fetchone()
            return self._row_to_usuario(row)

    @staticmethod
    def _row_to_usuario(row) -> Usuario:
        """Converte uma Row do SQLAlchemy para a entidade de domínio Usuario."""
        data = dict(row._mapping)
        return Usuario(
            id=data["id"],
            nome=data["nome"],
            email=data["email"],
            senha_hash=data["senha_hash"],
            data_cadastro=data["data_cadastro"],
            tipo_conta=data["tipo_conta"],
        )
