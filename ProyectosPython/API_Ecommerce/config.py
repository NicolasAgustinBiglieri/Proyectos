import os
from dotenv import load_dotenv

load_dotenv()  # Cargar variables de entorno desde el archivo .env

class Settings:
    SECRET: str = os.getenv("SECRET")
    EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_DURATION: int = int(os.getenv("ACCESS_TOKEN_DURATION"))

settings = Settings()