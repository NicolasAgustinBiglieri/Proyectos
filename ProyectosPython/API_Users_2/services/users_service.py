from fastapi import HTTPException, status
from db.models.user import User, User_wPass
# from db.schemas.user import user_schema, user_pass_schema
from passlib.context import CryptContext
from db.logger_base import log
from db.cursor_pool import CursorDelPool

crypt = CryptContext(schemes="bcrypt")

# Búsqueda de usuarios para CRUD de users, raise si se no encuentra
# def search_user(field: str, key):
#     try:
#         user = user_schema(users_collection.find_one({field: key}))
#         return User(**user)
#     except:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "No se ha encontrado el usuario")
    
# def search_user_pass(field: str, key):
#     try:
#         user = user_pass_schema(users_collection.find_one({field: key}))
#         return User_wPass(**user)
#     except:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "No se ha encontrado el usuario")
    

# Búsqueda de usuarios para CRUD de users, raise si se no encuentra
# Nuevas versiones
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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "No se ha encontrado el usuario")
    
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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "No se ha encontrado el usuario")
    
# Búsqueda de todos los usuarios
def search_all_users():
    query = f"SELECT id, username, email, firstname, lastname, dateofbirth, country, city, email_verif, registered_date FROM users"
    try:
        with CursorDelPool() as cursor:
            cursor.execute(query)
            users = cursor.fetchall()
            all_users = []
            if users:
                for user in users:
                    user_dict = dict(zip([desc[0] for desc in cursor.description], user))
                    all_users.append(User(**user_dict))
            return all_users
    except Exception as e:
        log.error(f"Error al buscar usuarios: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "Surgió un error al buscar los usuarios")
    
    
# Nuevas funciones para los nuevos endpoints que quiero implementar/mejorar/reemplazar:
def change_user_password(user: User_wPass, new_password: str):
    """
    Cambia la contraseña de un usuario.
    """
    try:
        # Hasheamos la nueva contraseña
        hashed_password = crypt.hash(new_password)

        # Actualizamos la contraseña en la base de datos
        with CursorDelPool() as cursor:
            cursor.execute("""
                UPDATE users
                SET password = %s
                WHERE id = %s
                """, 
                (hashed_password, user.id))
            
            # Verificamos si se actualizó alguna fila
            if cursor.rowcount == 0:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
            
    except Exception as e:
        log.error(f"Error al cambiar la contraseña del usuario: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor")


