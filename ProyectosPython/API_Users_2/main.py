"""

On Linux/Mac:
    source venv/bin/activate  
On Windows:
    .venv\Scripts\Activate

If your Windows system has restrictions to activate the .env, use first:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

Web para la generación de correos electrónicos temporales: https://temp-mail.org/

Instalaciones para el entorno virtual (más allá de que tenemos requirements.txt):
pip install fastapi[all]
pip install psycopg2
pip install passlib
pip install python-jose
pip install pytest
pip install bcrypt



"""

from fastapi import FastAPI
from routers import users, auth

app = FastAPI()

# Routers

app.include_router(users.router)
app.include_router(auth.router)


# Operaciones

@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}

