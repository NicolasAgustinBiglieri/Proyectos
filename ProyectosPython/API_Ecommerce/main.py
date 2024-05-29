"""
Web para la generación de correos electrónicos temporales: https://temp-mail.org/

"""

from fastapi import FastAPI
from routers import users, auth

app = FastAPI()

# Routers

app.include_router(users.router)
app.include_router(auth.router)


# Operaciones

@app.get("/")
def root():
    return ("Bienvenido a Fakebook Marketplace")


