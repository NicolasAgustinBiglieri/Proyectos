from fastapi import APIRouter, HTTPException, Depends, status
from db.models.user import User, User_wPass, UserProfileUpdate, ChangePasswordRequest
# from db.schemas.user import users_schema
from services.users_service import search_user, search_user_pass, search_all_users, change_user_password
from services.auth_service import verify_pass, validate_date
from routers.auth import auth_user, is_admin
from db.logger_base import log
from db.cursor_pool import CursorDelPool
from passlib.context import CryptContext


router = APIRouter(prefix="/users", tags=["Users"])

crypt = CryptContext(schemes="bcrypt")

# Get para prueba de token de autorización temporal al loguear
@router.get("/me")
async def me(user: User = Depends(auth_user)):
    """
    Endpoint para que un usuario obtenga sus propios datos de usuario si está autenticado y autorizado

    Permite a un usuario obtener sus datos proporcionando el token que recibe al loguear
    """
    return user


# Operaciones CRUD

@router.get("/", response_model=list[User])
async def get_all_users(_: User = Depends(auth_user)):
    """
    Endpoint para obtener un listado de todos los usuarios
    """
    return search_all_users()

@router.get("/{id}")
async def get_user(id: int, _: User = Depends(auth_user)):
    """
    Endpoint para obtener un usuario

    Se debe proporcionar el id del usuario deseado
    """
    return search_user("id", id)

@router.get("/query/") 
async def get_user_query(id: int, _: User = Depends(auth_user)):
    """
    Endpoint para obtener un usuario por query

    Se debe proporcionar el id del usuario deseado
    """
    return search_user("id", id)


@router.put("/", response_model=User_wPass)
async def put_user(user: User_wPass, _: User = Depends(is_admin)):
    """
    Endpoint para actualizar un usuario

    Se debe proporcionar el usuario con todos sus campos completos, sean modificados o los actuales. Incluido el Id.
    
    Ejemplo de solicitud:
    {
        "id": 1,
        "username": "user123",
        "email": "user@example.com",
        "firstname": "John",
        "lastname": "Doe",
        "dateofbirth": "1990-01-01",
        "country": "Argentina",
        "city": "Buenos Aires",
        "email_verif": true,
        "registered_date": "2024-05-29T10:00:00",
        "role": "r_user",
        "password": "newpassword123"
    }
    
    Ejemplo de respuesta:
    {
        "id": 1,
        "username": "user123",
        "email": "user@example.com",
        "firstname": "John",
        "lastname": "Doe",
        "dateofbirth": "1990-01-01",
        "country": "Argentina",
        "city": "Buenos Aires",
        "email_verif": true,
        "registered_date": "2024-05-29T10:00:00"
        "role": "r_user",
        "password": "$2b$12$1234567890abcdefghij85mno"
    }
    """
    query = """
        UPDATE users
        SET username = %s, email = %s, firstname = %s, lastname = %s, dateofbirth = %s, country = %s, 
            city = %s, email_verif = %s, registered_date = %s, role = %s, password = %s
        WHERE id = %s
        RETURNING id, username, email, firstname, lastname, dateofbirth, country, city, 
        email_verif, registered_date, role, password
    """
    hashed_password = crypt.hash(user.password)
    values = (
        user.username, user.email, user.firstname, user.lastname, user.dateofbirth, user.country, 
        user.city, user.email_verif, user.registered_date, user.role, hashed_password, user.id
    )
    try:
        with CursorDelPool() as cursor:
            cursor.execute(query, values)
            updated_user = cursor.fetchone()
            if not updated_user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
            updated_user_dict = dict(zip([desc[0] for desc in cursor.description], updated_user))
            return User_wPass(**updated_user_dict)
    except Exception as e:
        log.error(f"Error al actualizar usuario: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")


@router.delete("/{id}")
async def del_user(id: int, _: User = Depends(is_admin)):
    """
    Endpoint para eliminar un usuario

    Se debe proporcionar el id del usuario a eliminar al final del path
    """
    query = "DELETE FROM users WHERE id = %s RETURNING id"
    
    try:
        with CursorDelPool() as cursor:
            cursor.execute(query, (id,))
            deleted_user = cursor.fetchone()
            if not deleted_user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
        return {"message": f"Usuario {deleted_user[0]} eliminado exitosamente"}
    except Exception as e:
        log.error(f"Error al eliminar usuario: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")



# A partir de acá van los nuevos endpoints que quiero implementar/mejorar/reemplazar:



# Endpoints para rol de usuario:

# Cambio de contraseña de un usuario
@router.put("/change-pass")
async def change_pass(request: ChangePasswordRequest, logged_user: User = Depends(auth_user)):
    """
    Endpoint para que un usuario cambie su contraseña.

    Se debe proporcionar la contraseña actual y la nueva contraseña.

    Ejemplo de solicitud:
    {
        "old_pass": "your_old_password",
        "new_pass": "your_new_password"
    }

    Ejemplo de respuesta:
    {
        "id": 1,
        "username": "user123",
        "email": "user@example.com",
        "firstname": "new_name",
        "lastname": "new_surname",
        "dateofbirth": "1990-01-01",
        "country": "Argentina",
        "city": "Buenos Aires",
        "email_verif": true,
        "registered_date": "2024-05-29T10:00:00"
    }
    """
    current_user = search_user_pass("id", logged_user.id)
    check_old_pass = verify_pass(request.old_pass, current_user.password)
    if not check_old_pass:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "La contraseña actual es incorrecta")
    change_user_password(current_user, request.new_pass)
    return search_user_pass("id", current_user.id) # {"message": "Contraseña actualizada correctamente"}


# Actualización de un usuario de su perfil
@router.put("/update-profile")
async def update_profile(profile_update: UserProfileUpdate, current_user: User = Depends(auth_user)):
    """
    Endpoint para que un usuario actualice su perfil.
    Puede actualizar únicamente los campos que se incluyen en el ejemplo de solicitud, o solo algunos de ellos.

    Ejemplo de solicitud:
    {
        "firstname": "new_name",
        "lastname": "new_surname",
        "dateofbirth": "1990-01-01",
        "country": "Argentina",
        "city": "Buenos Aires"
    }

    Ejemplo de respuesta:
    {
        "id": 1,
        "username": "user123",
        "email": "user@example.com",
        "firstname": "new_name",
        "lastname": "new_surname",
        "dateofbirth": "1990-01-01",
        "country": "Argentina",
        "city": "Buenos Aires",
        "email_verif": true,
        "registered_date": "2024-05-29T10:00:00"
    }
    """
    # Validación de dateofbirth
    if profile_update.dateofbirth and not validate_date(profile_update.dateofbirth):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="dateofbirth no es una fecha válida.")
    
    # Actualizar solo los campos proporcionados en el perfil del usuario
    update_dict = dict(profile_update.model_dump(exclude_unset=True))

    # Realizar la actualización en la base de datos
    # Utilizamos parámetros con nombres para mejorar la vulnerabilidad del endpoint
    # a SQL Injections
    query = """
        UPDATE users 
        SET firstname = %(firstname)s,
            lastname = %(lastname)s, dateofbirth = %(dateofbirth)s, 
            country = %(country)s, city = %(city)s
        WHERE id = %(id)s
        RETURNING id, username, email, firstname, lastname, dateofbirth, country, city, email_verif, registered_date, role
    """

    try:
        with CursorDelPool() as cursor:
            cursor.execute(query, {
                "firstname": update_dict.get("firstname", current_user.firstname),
                "lastname": update_dict.get("lastname", current_user.lastname),
                "dateofbirth": update_dict.get("dateofbirth", current_user.dateofbirth),
                "country": update_dict.get("country", current_user.country),
                "city": update_dict.get("city", current_user.city),
                "id": current_user.id
            })
            updated_user = cursor.fetchone()
            if not updated_user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
            
            updated_user_dict = dict(zip([desc[0] for desc in cursor.description], updated_user))
            return User(**updated_user_dict) # {"message": "Perfil actualizado correctamente"}
    except Exception as e:
        log.error(f"Error al actualizar perfil de usuario: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")



