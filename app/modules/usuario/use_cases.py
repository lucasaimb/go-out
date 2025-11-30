# app/modules/usuario/usecases.py
from app.modules.usuario.domain import Usuario, UsuarioRepository
import bcrypt


class CriarUsuarioUseCase:
    def __init__(self, repo: UsuarioRepository):
        self.repo = repo

    def executar(self, nome: str, email: str, senha: str) -> Usuario:
        senha_hash = bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt()).decode()
        return self.repo.criar(nome=nome, email=email, senha_hash=senha_hash)
