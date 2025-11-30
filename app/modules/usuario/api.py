# app/modules/usuario/api.py
from datetime import date
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.modules.usuario.domain import Usuario
from app.modules.usuario.infra import SqlAlchemyUsuarioRepository
from app.modules.usuario.use_cases import CriarUsuarioUseCase


router = APIRouter()


# ---------- Schemas Pydantic (entrada/saída) ----------

class UsuarioCreate(BaseModel):
    nome: str
    email: str
    senha: str


class UsuarioOut(BaseModel):
    id: int
    nome: str
    email: str
    data_cadastro: date
    tipo_conta: str


# ---------- Dependências simples ----------

def get_usuario_repo() -> SqlAlchemyUsuarioRepository:
    """
    Cria uma instância do repositório de usuários.
    Em projetos maiores você pode trocar isso por um container de DI.
    """
    return SqlAlchemyUsuarioRepository()


def get_criar_usuario_uc(
    repo: SqlAlchemyUsuarioRepository = Depends(get_usuario_repo),
) -> CriarUsuarioUseCase:
    return CriarUsuarioUseCase(repo)


# ---------- Helpers ----------

def usuario_to_out(usuario: Usuario) -> UsuarioOut:
    """Converte entidade de domínio para o schema de resposta."""
    return UsuarioOut(
        id=usuario.id,
        nome=usuario.nome,
        email=usuario.email,
        data_cadastro=usuario.data_cadastro,
        tipo_conta=usuario.tipo_conta,
    )


# ---------- Endpoints ----------

@router.get(
    "/",
    response_model=List[UsuarioOut],
    summary="Listar todos os usuários",
)
def listar_usuarios(
    repo: SqlAlchemyUsuarioRepository = Depends(get_usuario_repo),
) -> List[UsuarioOut]:
    usuarios = repo.listar()
    return [usuario_to_out(u) for u in usuarios]


@router.get(
    "/{usuario_id}",
    response_model=UsuarioOut,
    summary="Obter usuário pelo ID",
)
def obter_usuario_por_id(
    usuario_id: int,
    repo: SqlAlchemyUsuarioRepository = Depends(get_usuario_repo),
) -> UsuarioOut:
    usuario = repo.buscar_por_id(usuario_id)

    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return usuario_to_out(usuario)


@router.post(
    "/criar",
    response_model=UsuarioOut,
    status_code=201,
    summary="Criar novo usuário",
)
def criar_usuario(
    dados: UsuarioCreate,
    usecase: CriarUsuarioUseCase = Depends(get_criar_usuario_uc),
) -> UsuarioOut:
    usuario = usecase.executar(
        nome=dados.nome,
        email=dados.email,
        senha=dados.senha,
    )
    return usuario_to_out(usuario)
