from pydantic_settings import BaseSettings
from pathlib import Path
from pydantic import BaseModel

BASE_DIR = Path(__file__).parent.parent


class DBSettings(BaseModel):
    url: str = "postgresql+asyncpg://postgres:postgres@localhost/postgres"
    echo: bool = True


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algoritm: str = "RS256"
    access_token_expire_minutes: int = 15


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"

    db: DBSettings = DBSettings()
    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()
