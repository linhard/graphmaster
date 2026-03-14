from pydantic import BaseSettings

class Settings(BaseSettings):
    ORACLE_DSN: str
    ORACLE_USER: str
    ORACLE_PASSWORD: str

    class Config:
        env_file = ".env"
