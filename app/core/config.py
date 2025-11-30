from urllib.parse import quote_plus
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # Banco
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    # Configuração de como o Pydantic lê o .env
    model_config = SettingsConfigDict(
        env_file=r"C:\ProjetosPython\go-out\.env",
        env_file_encoding="utf-8"
    )

    @property
    def DATABASE_URL(self) -> str:
        password_escaped = quote_plus(self.DB_PASSWORD)
        return (
            f"postgresql+psycopg2://{self.DB_USER}:{password_escaped}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?sslmode=require"
        )


settings = Settings()
