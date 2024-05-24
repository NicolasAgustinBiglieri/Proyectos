import pytest
from fastapi.testclient import TestClient
from ..main import app

"""
Por el momento las operaciones son solo del CRUD.
Después habrá que hacerlo del user/me y auth_user o moverlas de archivo
"""

client = TestClient(app)


def test_get_users():
    # Creamos varios usuario
    create_several_users()
    # Obtenemos los usuarios
    response = client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_user():
    # Creamos un usuario
    user_id = create_one_user()["id"]
    # Obtenemos el usuario
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json().get("username") == "test_username"
    assert isinstance(response.json(), dict)


def test_get_user_query():
    # Creamos un usuario
    user_id = create_one_user()["id"]
    # Obtenemos el usuario
    response = client.get(f"/users/query/?id={user_id}")
    assert response.status_code == 200
    assert response.json().get("username") == "test_username"
    assert isinstance(response.json(), dict)


def test_update_user():
    # Creamos un usuario
    user = create_one_user()
    # Obtenemos el usuario
    response = client.get(f"/users/{user["id"]}")
    # Modificamos al usuario
    updated_user_data = user.copy()
    updated_user_data["firstname"] = 'Updated_Agu'
    updated_user_data["lastname"] = 'Updated_Uga'
    response = client.put("/users/", json=updated_user_data)
    assert response.status_code == 200
    assert response.json().get("firstname") == "Updated_Agu"


def test_delete_user():
    # Creamos un usuario
    user = create_one_user()
    # Obtenemos el usuario
    response = client.get(f"/users/{user["id"]}")
    # Eliminamos al usuario
    response = client.delete(f"/users/{user["id"]}")
    assert response.status_code == 200
    assert response.json() == None
    # Intentamos obtener el usuario y comprobar que devuelve None
    response = client.get(f"/users/{user["id"]}")
    assert response.status_code == 404
    response.json() == {'Error': 'No se ha encontrado el usuario'}

    







# Creamos varios usuarios para el test_get_users
def create_several_users():
    user_data = {
        "username": "test_username01","email": "test01@email.com","firstname": "Agu","lastname": "Uga",
        "dateofbirth": "1994-01-28","country": "Arg","city": "BsAs","password": "nico"
    }
    response = client.post("/register", json=user_data)
    user_data = {
        "username": "test_username02","email": "test02@email.com","firstname": "Agu","lastname": "Uga",
        "dateofbirth": "1994-01-28","country": "Arg","city": "BsAs","password": "nico"
    }
    response = client.post("/register", json=user_data)
    user_data = {
        "username": "test_username03","email": "test03@email.com","firstname": "Agu","lastname": "Uga",
        "dateofbirth": "1994-01-28","country": "Arg","city": "BsAs","password": "nico"
    }
    response = client.post("/register", json=user_data)


# Creamos un usuario para el test_get_user y test_get_user_query
def create_one_user():
    user_data = {
        "username": "test_username","email": "test01@email.com","firstname": "Agu","lastname": "Uga",
        "dateofbirth": "1994-01-28","country": "Arg","city": "BsAs","password": "nico"
    }
    response = client.post("/register", json=user_data)
    return response.json()
