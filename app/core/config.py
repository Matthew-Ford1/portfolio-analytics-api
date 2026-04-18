from pydantic import (
    SecretStr,
    computed_field,
)
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")  # checks current working directory

    SECRET_KEY: SecretStr
    TOKEN_EXPIRE_MINUTES: int = 7 * 24 * 60  # 7 days

    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr = ""
    POSTGRES_DB: str = ""

    @computed_field
    @property
    def DATABASE_URL(self) -> SecretStr:
        return SecretStr(
            f"{'postgresql+psycopg'}://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD.get_secret_value()}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}",
        )


config = Config()
