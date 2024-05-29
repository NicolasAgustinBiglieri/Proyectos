from fastapi import HTTPException, status
from bson import ObjectId
from db.client import users_collection
from db.schemas.user import user_pass_schema
from db.models.user import User, User_wPass
from db.schemas.user import user_schema, user_pass_schema


# Búsqueda de usuarios para CRUD de users, raise si se no encuentra
def search_user(field: str, key):
    try:
        user = user_schema(users_collection.find_one({field: key}))
        return User(**user)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "No se ha encontrado el usuario")
    
def search_user_pass(field: str, key):
    try:
        user = user_pass_schema(users_collection.find_one({field: key}))
        return User_wPass(**user)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "No se ha encontrado el usuario")
    
# Verificación de ObjectId y manejo de error
def verif_ObjectId(id):
    if ObjectId.is_valid(id):
        return id
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{id} is not a valid ObjectId")
    
    