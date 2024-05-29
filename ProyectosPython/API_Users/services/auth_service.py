from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
from db.client import users_collection
from db.models.user import User, User_wPass
from db.schemas.user import user_schema, user_pass_schema
from config import settings


crypt = CryptContext(schemes="bcrypt")

def verify_pass(normal_pass, hashed_pass):
    return crypt.verify(normal_pass, hashed_pass)

def authenticate_user(username: str, password: str):
    user_db = search_user_pass("username", username)
    if type(user_db) == User_wPass and verify_pass(password, user_db.password):
        return user_db
    return None
    
def create_access_token(username):
    expire = datetime.now(timezone.utc) + timedelta(minutes = settings.ACCESS_TOKEN_DURATION)
    access_token = {"sub": username, "exp": expire}
    return jwt.encode(access_token, settings.SECRET, algorithm=settings.ALGORITHM)


# Búsqueda de usuarios para registro y auth, si no encuentra devuelve None
def search_user(field: str, key):
    try:
        user = user_schema(users_collection.find_one({field: key}))
        return User(**user)
    except:
        return None
    
def search_user_pass(field: str, key):
    try:
        user = user_pass_schema(users_collection.find_one({field: key}))
        return User_wPass(**user)
    except:
        return None
    


