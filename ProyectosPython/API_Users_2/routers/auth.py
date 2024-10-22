from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import jwt, JWTError
from db.models.user import User_wPass, User, RoleEnum, ChangePasswordRequest, ResetPasswordRequest
# from db.schemas.user import user_pass_schema
from services.auth_service import authenticate_user, create_access_token, search_user, validate_date
from services.email_service import send_email_verification, create_verify_token, send_password_reset_email
from services.users_service import change_user_password
from config import settings
from db.logger_base import log
from db.cursor_pool import CursorDelPool
from psycopg2.errors import UniqueViolation

router = APIRouter(tags=["Auth"])

oauth2 = OAuth2PasswordBearer(tokenUrl="auth/login") 
crypt = CryptContext(schemes="bcrypt")


# Registro de usuario
@router.post("/register", response_model=User_wPass)
async def register(user: User_wPass):
    """
    Endpoint para registrar un nuevo usuario.

    Permite registrar un nuevo usuario con los datos proporcionados en el cuerpo de la solicitud.
    Devuelve los detalles del usuario registrado, incluido un identificador único asignado por el sistema.

    Web para la generación de correos electrónicos temporales: https://temp-mail.org/
    
    Ejemplo de solicitud:
    {
        "username": "user123",
        "email": "user@example.com",
        "firstname": "Name",
        "lastname": "Surname",
        "dateofbirth": "1990-01-01",
        "country": "Argentina",
        "city": "Buenos Aires",
        "password": "password123"
    }

    Ejemplo de respuesta:
    {
        "id": "1234567890",
        "username": "user123",
        "email": "user@example.com",
        "firstname": "Name",
        "lastname": "Surname",
        "dateofbirth": "1990-01-01",
        "country": "Argentina",
        "city": "Buenos Aires",
        "email_verif": False,
        "registered_date": "2024-05-29T10:00:00",
        "password": "$2b$12$1234567890abcdefghijklmno"
    }
    """
    # Verificar si el username ya está en uso
    if search_user("username", user.username):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El username ya está en uso")
    
    # Verificar si el email ya está en uso
    if search_user("email", user.email):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El email ya está en uso")
    
    # Validación de dateofbirth
    if user.dateofbirth and not validate_date(user.dateofbirth):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="dateofbirth no es una fecha válida.")
    
    try:
        # Hasheamos contraseña y la reemplazamos en la inserción 'INSERT TO'
        hashed_password = crypt.hash(user.password)

        with CursorDelPool() as cursor:
            cursor.execute("""
                INSERT INTO users (username, email, firstname, lastname, dateofbirth, country, city, password) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s) 
                RETURNING id, username, email, firstname, lastname, dateofbirth, country, city, email_verif, registered_date, password
                """, 
                (user.username, user.email, user.firstname, user.lastname, user.dateofbirth, user.country, user.city, hashed_password))
            new_user = cursor.fetchone()

        # Generar token de verificación para enviar email de verificación
        verification_token = create_verify_token(user.username, user.email)
        send_email_verification(user.email, verification_token)

        # Convertir el resultado de la consulta a un diccionario con nombres de columnas como claves
        new_user_dict = dict(zip([desc[0] for desc in cursor.description], new_user))

        return User_wPass(**new_user_dict)
    except UniqueViolation as e:
        log.error(f"Error al crear usuario: {e}")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El nombre de usuario o email ya está en uso")
    except Exception as e:
        log.error(f"Error al crear usuario: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")


# Ruta para verificar el token de verificación de registro
@router.get("/auth/verify")
async def verify_token(token: str):
    """
    Verifica el token de usuario y actualiza el campo email_verif a True si el token es válido.
    
    Args:
    - token: str: Token de verificación de usuario.
    
    Returns:
    - dict: Mensaje de éxito si el token es verificado correctamente.
    """
    try:
        payload = jwt.decode(token, settings.SECRET, algorithms=[settings.ALGORITHM])
        username = payload.get("username")
        user = search_user("username", username)

        if user and not user.email_verif:
            # Actualizar la verificación de correo en la base de datos
            with CursorDelPool() as cursor:
                cursor.execute("""
                    UPDATE users 
                    SET email_verif = TRUE 
                    WHERE username = %s AND email = %s
                    """, (user.username, user.email))
                if cursor.rowcount == 0:
                    raise HTTPException(status_code=404, detail="Usuario no encontrado o token inválido")
        
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario ya ha sido verificado o no se encontró")

    except JWTError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token inválido")
    except Exception as e:
        log.error(f"Error al verificar el token: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")

    return {"message": "Token verificado exitosamente"}


# Login
@router.post("/auth/login")
async def login(user_and_pass: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint para iniciar sesión y obtener un token de acceso.

    Permite a los usuarios iniciar sesión proporcionando su nombre de usuario y contraseña.
    Devuelve un token de acceso válido para autorizar las solicitudes posteriores.

    Ejemplo de solicitud:
    {
        "username": "your_username",
        "password": "your_password"
    }
    
    Returns:
    {
        "access_token": "eyJhbGfiOiJIUzI1NiIsInR5cCI6IkpXVCJ9
            .eyJzdWIiOiJ1c2VyMTIzIiwiZXyrIjoxNzE8NTE4NTg4fQ
            .DXg6NvH0FKNW_h6C2UYVnnt2Vav8FzUXA46cYJ7BwC4",
        "token_type": "bearer"
    }
    """
    check_user = authenticate_user(user_and_pass.username, user_and_pass.password)
    if not check_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "Usuario o contraseña incorrectos")
    if check_user.email_verif == False:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "Debe verificar la cuenta por email")
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


def is_admin(current_user: User = Depends(auth_user)):
    # print(f"Usuario logueado: {current_user.role}")
    # print(RoleEnum.R_ADMIN)
    # print(RoleEnum.R_ADMIN.value)
    if current_user.role != RoleEnum.R_ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to perform this action. Requires admin role."
        )
    return current_user



# Recuperación de contraseña olvidada
@router.post("/forgot-password")
async def forgot_password(email: str):
    """
    Endpoint para recuperar una contraseña olvidada.
    
    Se debe pasar el email perteneciente a la cuenta de la que se olvidó la contraseña.
    Se le debe enviar a dicho email un token con el cual ingresar la nueva contraseña.
    
    Ejemplo de solicitud:
    {
        "email": "your_email"
    }
    """
    if not search_user("email", email):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Usuario no encontrado")

    send_password_reset_email(email)
    return "A mail has sended to you with the instructions to reset your password."


@router.post("/reset-password")
async def reset_password(request: ResetPasswordRequest):
    """
    Endpoint para restablecer la contraseña utilizando un token de recuperación.

    Se debe pasar un token válido generado previamente para permitir el restablecimiento.
    Se debe proporcionar la nueva contraseña.

    Ejemplo de solicitud:
    {
        "token": "your_token_here",
        "new_pass": "your_new_password_here"
    }
    """
    try:
        payload = jwt.decode(request.token, settings.SECRET, algorithms=[settings.ALGORITHM])
        username = payload.get("username")
        email = payload.get('email')

        # Verificar si el usuario existe 
        user = search_user("email", email)
        if not user or user.username != username:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado.")

        # Cambiar la contraseña del usuario
        change_user_password(user, request.new_pass)

        return {"message": "Contraseña actualizada correctamente"}

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    except Exception as e:
        log.error(f"Error al verificar el token: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")


