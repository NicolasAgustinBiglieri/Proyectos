from fastapi import APIRouter, HTTPException, Depends, status
from db.models.user import User, User_wPass
from db.schemas.user import users_schema
from db.client import users_collection
from services.users_service import search_user, search_user_pass, verif_ObjectId
from routers.auth import auth_user
from bson import ObjectId


router = APIRouter(prefix="/users", tags=["Users"])

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
async def get_users():
    """
    Endpoint para obtener un listado de todos los usuarios
    """
    return users_schema(users_collection.find())

@router.get("/{id}")
async def get_user(id: str):
    """
    Endpoint para obtener un usuario

    Se debe proporcionar el id del usuario deseado
    """
    return search_user("_id", ObjectId(verif_ObjectId(id)))

@router.get("/query/") 
async def get_user_query(id: str):
    """
    Endpoint para obtener un usuario por query

    Se debe proporcionar el id del usuario deseado
    """
    return search_user("_id", ObjectId(verif_ObjectId(id)))


@router.put("/", response_model=User_wPass)
async def put_user(user: User_wPass):
    """
    Endpoint para actualizar un usuario

    Se debe proporcionar el usuario con todos sus campos completos, sean modificados o los actuales. Incluido el Id.
    """
    user_dict = dict(user)
    del user_dict["id"]
    try:
        users_collection.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se ha actualizado")
    return search_user_pass("_id", ObjectId(user.id))

@router.delete("/{id}")
async def del_user(id: str):
    """
    Endpoint para eliminar un usuario

    Se debe proporcionar el id del usuario a eliminar
    """
    if not users_collection.find_one_and_delete({"_id": ObjectId(id)}):
        return {"Error":"No se ha eliminado el usuario"}


