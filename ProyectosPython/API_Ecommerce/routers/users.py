from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from db.models.user import User, User_wPass
from db.schemas.user import user_schema, users_schema, user_pass_schema
from db.client import db_client
from bson import ObjectId
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
from datetime import datetime


router = APIRouter(prefix="/users", tags=["Users"])


load_dotenv() # Cargamos variables de entorno
SECRET = os.getenv("SECRET") # Guardamos la semilla en la variable que utilizaremos

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
    

# Login

oauth2 = OAuth2PasswordBearer(tokenUrl="auth/login") 
# Creamos el algoritmo de encriptación 
ALGORITHM = "HS256" 
# Ponemos duración del access token para cuando el post devuelva el access token
ACCESS_TOKEN_DURATION = 1

# Creamos semilla para la encriptacion utilizando "openssl rand -hex 32" en una terminal
# La semilla la guardamos en .env, el cual está agregado a .gitignore para protegerlo

# Creamos contexto de encriptación. Cuando verifiquemos la contraseña ingresada 
# con la encriptada en la base de datos con crypt.verify usaremos este esquema
crypt = CryptContext(schemes="bcrypt")

# Creamos una operación de autenticación para enviar usuario y contraseña
# A la función login le ponemos el parámetro form de tipo OAuth2PasswordRequestForm


async def auth_user(token: str = Depends(oauth2)):
    
    exception = HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail="Credenciales de autenticación inválidas",
                    headers={"WWW-Authenticate": "Bearer"})
    try:
        username = jwt.decode(token, SECRET, algorithms= ALGORITHM).get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Credenciales inválidas")
    except JWTError:
        raise exception

    return search_user("username", username)

@router.get("/me")
async def me(user: User = Depends(auth_user)):
    return user


# Operaciones CRUD

@router.get("/", response_model=list[User])
async def users():
    return users_schema(db_client.find())

@router.get("/{id}")
async def user(id: str):
    return search_user("_id", ObjectId(id))

@router.get("/") # No funciona la query, averiguar porqué me devuelve todos los users
async def user(id: str):
    return search_user("_id", ObjectId(id))


@router.put("/", response_model=User_wPass)
async def user(user: User_wPass):

    user_dict = dict(user)
    del user_dict["id"]
    try:
        db_client.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se ha actualizado")
    return search_user_pass("_id", ObjectId(user.id))

@router.delete("/{id}")
async def user(id: str):
    if not db_client.find_one_and_delete({"_id": ObjectId(id)}):
        return {"Error":"No se ha eliminado el usuario"}






