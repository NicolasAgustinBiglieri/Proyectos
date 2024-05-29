from pydantic import BaseModel, Field
from datetime import datetime

class User(BaseModel):
    """
    Modelo de datos para un usuario.

    Contiene los detalles de un usuario registrado en el sistema.
    """
    id: str = None
    username: str
    email: str
    firstname: str
    lastname: str
    dateofbirth: datetime
    country: str
    city: str
    email_verif: bool = False
    registered_date: datetime = Field(default_factory=datetime.now)

class User_wPass(User):
    """
    Modelo de datos para un usuario con contraseña.

    Es el modelo de usuario base, pero incluye la contraseña del usuario.
    """
    password: str

