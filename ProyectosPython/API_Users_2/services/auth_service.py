from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
from db.models.user import User, User_wPass
# from db.schemas.user import user_schema, user_pass_schema
from config import settings
from db.logger_base import log
from db.cursor_pool import CursorDelPool


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

def validate_date(date_value: datetime) -> bool:
    # print(date_value)
    # print(datetime.now())
    if date_value > datetime.now():
        print("is false")
        return False
    return True


# Búsqueda de usuarios para registro y auth, si no encuentra devuelve None
def search_user(field: str, key):
    query = f"SELECT id, username, email, firstname, lastname, dateofbirth, country, city, email_verif, registered_date, role FROM users WHERE {field} = %s"
    try:
        with CursorDelPool() as cursor:
            cursor.execute(query, (key,))
            user = cursor.fetchone()
            if user:
                user_dict = dict(zip([desc[0] for desc in cursor.description], user))
                return User(**user_dict)
    except Exception as e:
        log.error(f"Error al buscar usuario: {e}")
        return None

def search_user_pass(field: str, key):
    query = f"SELECT id, username, email, firstname, lastname, dateofbirth, country, city, email_verif, registered_date, role, password FROM users WHERE {field} = %s"
    try:
        with CursorDelPool() as cursor:
            cursor.execute(query, (key,))
            user = cursor.fetchone()
            if user:
                user_dict = dict(zip([desc[0] for desc in cursor.description], user))
                return User_wPass(**user_dict)
    except Exception as e:
        log.error(f"Error al buscar usuario: {e}")
        return None

