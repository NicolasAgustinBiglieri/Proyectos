from fastapi import APIRouter, HTTPException, Depends
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
import secrets


router = APIRouter(prefix="/users", tags=["Users"])
router_auth = APIRouter()

# Registro de usuarios
@router_auth.post("/register", response_model=User_wPass)
async def register(user: User_wPass):
    if type(search_user_pass("username", user.username)) == User_wPass:
        raise HTTPException(status_code=404, detail="El username ya está en uso")
    elif type(search_user_pass("email", user.email)) == User_wPass:
        raise HTTPException(status_code=404, detail="El email ya está en uso")
    else:
        user_dict = dict(user)
        del user_dict["id"]
        
        hash_pass = crypt.hash(user.password) # hasheamos la contraseña
        user_dict["password"] = hash_pass # Reemplazamos la contraseña por la hasheada


        # # Generar token de verificación único para verificar registro
        # verification_token = secrets.token_urlsafe(32)
        # user_dict["verification_token"] = verification_token

        # # Enviar correo electrónico de verificación
        # send_email_verification(user.email, verification_token)


        # Insertamos el usuario en la base de datos con la contraseña hasheada
        # y sin el id, ya que la proxima función agrega un id
        id = db_client.insert_one(user_dict).inserted_id 


        # db_client.find_one_and_replace({"_id": ObjectId(id)}, hash_pass)

        return user_pass_schema(db_client.find_one({"_id": ObjectId(id)}))


# Correo de confirmación de registro
def send_email_verification(email, token):
    sender_email = "fakebookdarketplace@gmail.com"
    password = "mi contraseña"

    subject = "Verificación de registro"
    body = f"Por favor, haga clic en el siguiente enlace para verificar su registro: http://tu_app.com/verify?token={token}"

    message = MIMEMultipart()
    message["from"] = sender_email
    message["To"] = email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, email, message.as_string())

        
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
SECRET = "42d8d511d3471e4ee7cadfd31be2f620018ec472bb4a163eed86527c548932ad"
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
        raise HTTPException(status_code=400, detail= "El usuario es incorrecto")
    # Recuperamos el usuario que se encuentra en la base de datos (con la contraseña cifrada)
    user_db = search_user_pass("username", user_pass.username)
    
    # Desencriptamos contraseña
    try:
        if not crypt.verify(user_pass.password, user_db.password, scheme= "bcrypt"):
            raise HTTPException(status_code=400, detail= "La contraseña es incorrecta")
    except:
        raise HTTPException(status_code=400, detail= "Error al verificar contraseña")
    
    expire = datetime.now(timezone.utc) + timedelta(minutes = ACCESS_TOKEN_DURATION)

    access_token = {"sub": user_db.username, "exp": expire}

    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}


async def auth_user(token: str = Depends(oauth2)):
    
    exception = HTTPException(
                    status_code=401, 
                    detail="Credenciales de autenticación inválidas",
                    headers={"WWW-Authenticate": "Bearer"})
    try:
        username = jwt.decode(token, SECRET, algorithms= ALGORITHM).get("sub")
        if username is None:
            raise HTTPException(status_code=400, detail= "Credenciales inválidas")
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
        raise HTTPException(status_code=404, detail="No se ha actualizado")
    return search_user_pass("_id", ObjectId(user.id))

@router.delete("/{id}")
async def user(id: str):
    if not db_client.find_one_and_delete({"_id": ObjectId(id)}):
        return {"Error":"No se ha eliminado el usuario"}






