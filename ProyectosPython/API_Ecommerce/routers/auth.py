from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import jwt, JWTError
from db.models.user import User_wPass
from db.schemas.user import user_pass_schema
from db.client import users_collection
from services.auth_service import authenticate_user, create_access_token
from services.email_service import send_email_verification, create_verify_token
from services.auth_service import search_user, search_user_pass
from bson import ObjectId
from config import settings

router = APIRouter(tags=["Auth"])

oauth2 = OAuth2PasswordBearer(tokenUrl="auth/login") 
crypt = CryptContext(schemes="bcrypt")

# Registro de usuarios
@router.post("/register", response_model=User_wPass)
async def register(user: User_wPass):
    # Verificar si el username ya está en uso
    if search_user_pass("username", user.username):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El username ya está en uso")
    
    # Verificar si el email ya está en uso
    if search_user_pass("email", user.email):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El email ya está en uso")
    
    # Preparar el diccionario del usuario excluyendo el campo id
    user_dict = dict(user)
    del user_dict["id"]

    # Hashear contraseña y la reemplazamos
    user_dict["password"] = crypt.hash(user.password)

    # Generar token de verificación para enviar email de verificación
    verification_token = create_verify_token(user.username, user.email)
    send_email_verification(user.email, verification_token)

    # Insertar el usuario en la base de datos
    id = users_collection.insert_one(user_dict).inserted_id

    return user_pass_schema(users_collection.find_one({"_id": ObjectId(id)}))

# Ruta para verificar el token de verificación de registro
@router.get("/auth/verify")
async def verify_token(token: str):
    # Desencriptamos el token de verificación y si la info es correcta 
    # se actualiza la variable email_verif del usuario a True
    try:
        username = jwt.decode(token, settings.SECRET, algorithms= settings.ALGORITHM).get("username")
        user = search_user("username", username)
        if user and not user.email_verif:
            users_collection.find_one_and_update({"username": user.username},
                                          {'$set': {"email_verif": True}})
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ha surgido un error al verificar")
            
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se ha logrado verificar")

    return {"message": "Token verificado exitosamente"}


@router.post("/auth/login")
async def login(user_pass: OAuth2PasswordRequestForm = Depends()):
    check_user = authenticate_user(user_pass.username, user_pass.password)
    if not check_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "Usuario o contraseña incorrectos")
    access_token = create_access_token(check_user.username)
    return {"access_token": access_token, "token_type": "bearer"}


async def auth_user(token: str = Depends(oauth2)):
    
    exception = HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail="Credenciales de autenticación inválidas",
                    headers={"WWW-Authenticate": "Bearer"})
    try:
        username = jwt.decode(token, settings.SECRET, algorithms= settings.ALGORITHM).get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Credenciales inválidas")
    except JWTError:
        raise exception

    return search_user("username", username)

