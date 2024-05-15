from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
from db.client import db_client
from db.schemas.user import user_pass_schema
from dotenv import load_dotenv
from db.models.user import User, User_wPass
from db.schemas.user import user_schema, users_schema, user_pass_schema
import os


crypt = CryptContext(schemes="bcrypt")
ALGORITHM = "HS256" 
ACCESS_TOKEN_DURATION = 1

load_dotenv() # Cargamos variables de entorno
SECRET = os.getenv("SECRET") # Guardamos la semilla en la variable que utilizaremos


def verify_pass(normal_pass, hashed_pass):
    return crypt.verify(normal_pass, hashed_pass)

def authenticate_user(username: str, password: str):
    user_db = search_user_pass("username", username)
    print(user_db)
    if type(user_db) == User_wPass and verify_pass(password, user_db.password):
        return user_db
    return None
    
def create_access_token(username):
    expire = datetime.now(timezone.utc) + timedelta(minutes = ACCESS_TOKEN_DURATION)
    access_token = {"sub": username, "exp": expire}
    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}


# Búsqueda de usuarios

def search_user(field: str, key):
    try:
        user = user_schema(db_client.find_one({field: key}))
        return User(**user)
    except:
        return {"Error": "No se ha encontrado el usuario"}
    
def search_user_pass(field: str, key):
    try:
        user = user_pass_schema(db_client.find_one({field: key}))
        return User_wPass(**user)
    except:
        return {"Error": "No se ha encontrado el usuario"}
    


