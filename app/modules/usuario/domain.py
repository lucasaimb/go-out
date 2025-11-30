# app/modules/usuario/domain.py
from dataclasses import dataclass
from typing import Optional, Protocol, List
import datetime


@dataclass
class Usuario:
    id: int
    nome: str
    email: str
    senha_hash: str
    data_cadastro: datetime.date
    tipo_conta: str

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "senha_hash": self.senha_hash,
            "data_cadastro": self.data_cadastro,  # ou .isoformat()
            "tipo_conta": self.tipo_conta,
        }


class UsuarioRepository(Protocol):
    """Contrato que qualquer implementação de repositório deve seguir."""

    def listar(self) -> List[Usuario]:
        ...

    def buscar_por_id(self, usuario_id: int) -> Optional[Usuario]:
        ...

    def criar(
        self,
        nome: str,
        email: str,
        senha_hash: str,
        tipo_conta: str = "usuario",
    ) -> Usuario:
        ...
