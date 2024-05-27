from fastapi.testclient import TestClient

"""
Por practicidad en el código. El test del endpoint "users/me", el cual verifica el token
para terminar de loguear, se realiza en el archivo "test_auth"
"""

# $env:PYTHONPATH = "."; pytest -v -s # Utilizo esta linea al comienzo para darle el path a la terminal



def test_get_users(test_app: TestClient):
    # Creamos varios usuario
    create_several_users(test_app)
    # Obtenemos los usuarios
    response = test_app.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_user(test_app: TestClient):
    # Creamos un usuario
    user_id = create_one_user(test_app)["id"]
    # Obtenemos el usuario
    response = test_app.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json().get("username") == "test_username"
    assert isinstance(response.json(), dict)


def test_get_user_query(test_app: TestClient):
    # Creamos un usuario
    user_id = create_one_user(test_app)["id"]
    # Obtenemos el usuario
    response = test_app.get(f"/users/query/?id={user_id}")
    assert response.status_code == 200
    assert response.json().get("username") == "test_username"
    assert isinstance(response.json(), dict)


def test_update_user(test_app: TestClient):
    # Creamos un usuario
    user = create_one_user(test_app)
    # Obtenemos el usuario
    response = test_app.get(f"/users/{user["id"]}")
    # Modificamos al usuario
    updated_user_data = user.copy()
    updated_user_data["firstname"] = 'Updated_Agu'
    updated_user_data["lastname"] = 'Updated_Uga'
    response = test_app.put("/users/", json=updated_user_data)
    assert response.status_code == 200
    assert response.json().get("firstname") == "Updated_Agu"


def test_delete_user(test_app: TestClient):
    # Creamos un usuario
    user = create_one_user(test_app)
    # Obtenemos el usuario
    response = test_app.get(f"/users/{user["id"]}")
    # Eliminamos al usuario
    response = test_app.delete(f"/users/{user["id"]}")
    assert response.status_code == 200
    assert response.json() == None
    # Intentamos obtener el usuario y comprobar que devuelve None
    response = test_app.get(f"/users/{user["id"]}")
    assert response.status_code == 404
    response.json() == {'Error': 'No se ha encontrado el usuario'}

    








# Creamos varios usuarios para el test_get_users
def create_several_users(test_app: TestClient):
    user_data = {
        "username": "test_username01","email": "test01@email.com","firstname": "Agu","lastname": "Uga",
        "dateofbirth": "1994-01-28","country": "Arg","city": "BsAs","password": "nico"
    }
    response = test_app.post("/register", json=user_data)
    user_data = {
        "username": "test_username02","email": "test02@email.com","firstname": "Agu","lastname": "Uga",
        "dateofbirth": "1994-01-28","country": "Arg","city": "BsAs","password": "nico"
    }
    response = test_app.post("/register", json=user_data)
    user_data = {
        "username": "test_username03","email": "test03@email.com","firstname": "Agu","lastname": "Uga",
        "dateofbirth": "1994-01-28","country": "Arg","city": "BsAs","password": "nico"
    }
    response = test_app.post("/register", json=user_data)


# Creamos un usuario para el test_get_user y test_get_user_query
def create_one_user(test_app: TestClient):
    user_data = {
        "username": "test_username","email": "test01@email.com","firstname": "Agu","lastname": "Uga",
        "dateofbirth": "1994-01-28","country": "Arg","city": "BsAs","password": "nico"
    }
    response = test_app.post("/register", json=user_data)
    return response.json()
