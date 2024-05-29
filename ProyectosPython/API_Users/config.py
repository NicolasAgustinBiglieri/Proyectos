import os
from dotenv import load_dotenv

load_dotenv()  # Cargar variables de entorno desde el archivo .env

class Settings:
    SECRET: str = os.getenv("SECRET")
    ALGORITHM: str = os.getenv("ALGORITHM")
    ACCESS_TOKEN_DURATION: int = int(os.getenv("ACCESS_TOKEN_DURATION"))
    EMAIL_ACCOUNT: str = os.getenv("EMAIL_ACCOUNT")
    EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD")

    TEST_DATABASE_URL: str = "mongodb://localhost:27017/test_database"

settings = Settings()

