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
router_auth = APIRouter()

load_dotenv() # Cargamos variables de entorno
SECRET = os.getenv("SECRET") # Guardamos la semilla en la variable que utilizaremos

# Registro de usuarios
@router_auth.post("/register", response_model=User_wPass)
async def register(user: User_wPass):
    if type(search_user_pass("username", user.username)) == User_wPass:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El username ya está en uso")
    elif type(search_user_pass("email", user.email)) == User_wPass:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El email ya está en uso")
    else:
        if not user.registered_date:
            user.registered_date = datetime.now() # Colocamos fecha de registro now
        user_dict = dict(user)
        del user_dict["id"]
        
        hash_pass = crypt.hash(user.password) # hasheamos la contraseña
        user_dict["password"] = hash_pass # Reemplazamos la contraseña por la hasheada


        # Generar token de verificación único para verificar registro
        token = {
            "username": user.username,
            "email": user.email
        }
        verification_token = jwt.encode(token, SECRET, algorithm=ALGORITHM)

        # Enviar correo electrónico de verificación
        send_email_verification(user.email, verification_token)

        # Insertamos el usuario en la base de datos con la contraseña hasheada
        # y sin el id, ya que la proxima función agrega un id
        id = db_client.insert_one(user_dict).inserted_id 


        return user_pass_schema(db_client.find_one({"_id": ObjectId(id)}))


# Correo de confirmación de registro
def send_email_verification(email, token):
    sender_email = "aguprograma@gmail.com"
    password = os.getenv("EMAIL_PASSWORD")

    subject = "Verificación de registro"
    body = f"Por favor, haga clic en el siguiente enlace para verificar su registro: http://127.0.0.1:8000/verify?token={token}"

    message = MIMEMultipart()
    message["from"] = sender_email
    message["To"] = email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, email, message.as_string())

        
# Ruta para verificar el token de verificación de registro
@router_auth.get("/verify")
async def verify_token(token: str):
    # Desencriptamos el token de verificación y si la info es correcta 
    # se actualiza la variable email_verif del usuario a True
    try:
        username = jwt.decode(token, SECRET, algorithms= ALGORITHM).get("username")
        user = search_user("username", username)
        if user and not user.email_verif:
            db_client.find_one_and_update({"username": user.username},
                                          {'$set': {"email_verif": True}})
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ha surgido un error al verificar")
            
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se ha logrado verificar")

    # Si la verificación es exitosa, puedes redirigir al usuario a una página de éxito
    # Puedes usar plantillas HTML para renderizar una página de éxito o simplemente devolver un mensaje JSON
    return {"message": "Token verificado exitosamente"}



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

oauth2 = OAuth2PasswordBearer(tokenUrl="login") 
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
@router_auth.post("/login")
async def login(user_pass: OAuth2PasswordRequestForm = Depends()):
    # Comprobamos si tenemos el usuario ingresado
    check_user = search_user("username", user_pass.username)
    if not type(check_user) == User: # Si el usuario no se encuentra, la búsqueda devuelve un diccionario de error
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "El usuario es incorrecto")
    # Recuperamos el usuario que se encuentra en la base de datos (con la contraseña cifrada)
    user_db = search_user_pass("username", user_pass.username)
    
    # Desencriptamos contraseña
    try:
        if not crypt.verify(user_pass.password, user_db.password, scheme= "bcrypt"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "La contraseña es incorrecta")
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "Error al verificar contraseña")
    
    expire = datetime.now(timezone.utc) + timedelta(minutes = ACCESS_TOKEN_DURATION)

    access_token = {"sub": user_db.username, "exp": expire}

    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}


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






