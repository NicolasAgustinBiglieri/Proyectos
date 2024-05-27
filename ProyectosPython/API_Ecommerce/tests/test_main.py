import pytest


# $env:PYTHONPATH = "."; pytest -v -s # Utilizo esta linea al comienzo para darle el path a la terminal



# Testeamos la raíz de la web.
@pytest.mark.usefixtures("test_app") 
# Usa @pytest.mark.usefixtures cuando necesitas que el fixture se ejecute pero no necesitas el valor del fixture en la función de prueba
# En este caso no es necesario pero lo dejo para tener esta información a mano
def test_read_root(test_app):
    response = test_app.get("/")
    assert response.status_code == 200
    assert response.json() == "Bienvenido a Fakebook Marketplace"
    

# # Testeamos el registro de un usuario
# def test_register_user(test_app):
#     user_data = {
#         "username": "test_username",
#         "email": "test@email.com",
#         "firstname": "Agu",
#         "lastname": "Uga",
#         "dateofbirth": "1994-01-28",
#         "country": "Arg",
#         "city": "BsAs",
#         "password": "nico"
#     }
#     response = test_app.post("/register", json=user_data)
#     # print(response.json())
#     assert response.status_code == 200
#     assert "id" in response.json()
#     assert response.json()["username"] == "test_username"
    

