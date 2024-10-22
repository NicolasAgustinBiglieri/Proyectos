from fastapi.testclient import TestClient
from ..services.email_service import create_verify_token

# $env:PYTHONPATH = "."; pytest -v -s # Utilizo esta linea al comienzo para darle el path a la terminal


# Testeamos el registro de un usuario
def test_register_user(test_app: TestClient):
    # Registramos usuario
    response = register_user(test_app)
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["username"] == "test_username"


# Testeamos la verificación del token de verificación de registro
def test_register_token_verification(test_app: TestClient):
    # Registramos un usuario
    user_registered = register_user(test_app).json()
    # Generamos el token
    verification_token = create_verify_token("test_username", "test@email.com")
    # Verificamos el token enviado por email
    response = test_app.get("/auth/verify", params={"token": verification_token})
    assert response.status_code == 200
    assert response.json() == {"message": "Token verificado exitosamente"}
    # Obtenemos el user por un get para chequear el campo "email_verif"
    response = test_app.get(f"/users/{user_registered["id"]}")
    assert response.json()["email_verif"]


# Testeamos el login
def test_login(test_app: TestClient):
    # Registramos un usuario
    user_registered = register_user(test_app).json()
    # Creamos los datos para pasar de tipo OAuth2PasswordRequestForm
    login_data = {
        "username": user_registered["username"],
        "password": "test_password"
    }
    # Ejecutamos el endpoint de login, el cual devuelve un token 
    response = test_app.post("/auth/login", data=login_data)
    assert response.status_code == 200
    assert response.json()["access_token"]
    assert response.json()["token_type"] == "bearer"


# Testeamos la verificación de token al loguear
def test_user_me(test_app: TestClient):
    # Registramos un usuario
    user_registered = register_user(test_app).json()
    # Creamos los datos para pasar de tipo OAuth2PasswordRequestForm
    login_data = {
        "username": user_registered["username"],
        "password": "test_password"
    }
    # Ejecutamos el endpoint de login, el cual devuelve un token 
    response = test_app.post("/auth/login", data=login_data)
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = test_app.get("/users/me", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), dict)







# Función para registrar usuarios. Devuelve el usuario en un json o dict con id y todo lo que se le agrega
def register_user(test_app: TestClient):
    user_data = {
        "username": "test_username",
        "email": "test@email.com",
        "firstname": "test_firstname",
        "lastname": "test_lastname",
        "dateofbirth": "1990-01-01",
        "country": "test_country",
        "city": "test_city",
        "password": "test_password"
    }
    response = test_app.post("/register", json=user_data)
    return response




