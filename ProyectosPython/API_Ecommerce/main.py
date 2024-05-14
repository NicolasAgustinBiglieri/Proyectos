"""
Comenzamos proyecto de API Ecommerce con FastAPI Python

1: Planificar una API:

-Establecer un caso de uso
-Comenzar con una especificación (buscar OpenAPI)
-Describir requisitos

2: Diseño y Prototipo: # Confiabilidad, seguridad, capacidad de escalamiento

-Crear diagrama de flujo de la API
-Incluir seguridad en el diseño (identificación, autenticación, autorización y cifrado)
-Decidir qué arquitectura se utilizará (SOAP o REST) -> REST
-Planificar portal para desarrolladores ?¿?¿
-Crear el prototipo

3: Desarrollar
4: Probar
5: Entregar
6: Monitorear e iterar


*** Vamos a probar hacer una API para manejar algo parecido a un Facebook Marketplace
donde registrar usuarios, que se verifiquen con el email, puedan agregar productos, ver productos

En un segundo paso, implementar un chat para esos usuarios

En un tercer paso, que puedan comprar los productos



https://temp-mail.org/

"""

from fastapi import FastAPI
from routers import users

app = FastAPI()

# Routers

app.include_router(users.router)
app.include_router(users.router_auth)


# Operaciones

@app.get("/")
def root():
    return ("Bienvenido a Fakebook Marketplace")


