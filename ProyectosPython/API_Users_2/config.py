import os
from dotenv import load_dotenv

load_dotenv()  # Cargar variables de entorno desde el archivo .env

class Settings:
    SECRET: str = os.getenv("SECRET")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_DURATION: int = int(os.getenv("ACCESS_TOKEN_DURATION"))
    EMAIL_ACCOUNT: str = os.getenv("EMAIL_ACCOUNT")
    EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD")

    _DATABASE: str = os.getenv("_DATABASE")
    _USERNAME: str = os.getenv("_USERNAME")
    _PASSWORD: str = os.getenv("_PASSWORD")
    _DB_PORT: int = int(os.getenv("_DB_PORT"))
    _HOST: str = os.getenv("_HOST")
    _MIN_CON: int = int(os.getenv("_MIN_CON"))
    _MAX_CON: int = int(os.getenv("_MAX_CON"))
    _pool= os.getenv("_pool")
    if _pool == "None":
        _pool = None  # Convertir "None" de str a NoneType


settings = Settings()

