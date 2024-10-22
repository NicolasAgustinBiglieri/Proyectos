import pytest


# $env:PYTHONPATH = "."; pytest -v -s # Utilizo esta linea al comienzo para darle el path a la terminal



# Testeamos la raíz de la web.
@pytest.mark.usefixtures("test_app") 
# Usa @pytest.mark.usefixtures cuando necesitas que el fixture se ejecute pero no necesitas el valor del fixture en la función de prueba
# En este caso no es necesario pero lo dejo para tener esta información a mano
def test_read_root(test_app):
    response = test_app.get("/")
    assert response.status_code == 200
    assert response.json() == "Welcome to the API"

