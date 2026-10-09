import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "mysql+pymysql://root:@localhost:3306/rios_pastries")
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY", "clave_secreta_rios_pastries_2024")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    APP_NAME: str = os.getenv("APP_NAME", "API Ríos Pastries")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"


settings = Settings()


def get_settings():
    return settings
