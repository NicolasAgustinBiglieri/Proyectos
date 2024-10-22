from pydantic import BaseModel, Field, EmailStr, StringConstraints, constr
from datetime import datetime
from typing import Annotated
from enum import Enum

class RoleEnum(str, Enum):
    R_USER = "r_user"
    R_ADMIN = "r_admin"

# Definimos las restricciones para las cadenas de texto
UsernameType = Annotated[str, StringConstraints(min_length=3, max_length=50, pattern=r'^[a-zA-Z0-9_]+$')]
FirstnameType = Annotated[str, StringConstraints(min_length=1, max_length=50, pattern=r'^[a-zA-Z]+$')]
LastnameType = Annotated[str, StringConstraints(min_length=1, max_length=50, pattern=r'^[a-zA-Z]+$')]
CountryType = Annotated[str, StringConstraints(min_length=2, max_length=50, pattern=r'^[a-zA-Z\s]+$')]
CityType = Annotated[str, StringConstraints(min_length=1, max_length=50, pattern=r'^[a-zA-Z\s]+$')]
PasswordType = Annotated[str, StringConstraints(min_length=8, max_length=128, pattern=r"^[A-Za-z0-9_\d@$!%*./?&]+$")]

class User(BaseModel):
    """
    Modelo de datos para un usuario.

    Contiene los detalles de un usuario registrado en el sistema.
    """
    # id: int = None
    # username: str
    # email: str
    # firstname: str
    # lastname: str
    # dateofbirth: datetime
    # country: str
    # city: str
    # email_verif: bool = False
    # registered_date: datetime = Field(default_factory=datetime.now)
    # role: RoleEnum = RoleEnum.R_USER

    id: int = None
    username: UsernameType
    email: EmailStr
    firstname: FirstnameType
    lastname: LastnameType
    dateofbirth: datetime
    country: CountryType
    city: CityType
    email_verif: bool = False
    registered_date: datetime = Field(default_factory=datetime.now)
    role: RoleEnum = RoleEnum.R_USER
    
    class Config:
        extra = 'forbid'

class User_wPass(User):
    """
    Modelo de datos para un usuario con contraseña.

    Es el modelo de usuario base, pero incluye la contraseña del usuario.
    """
    # password: str

    password: PasswordType

class UserProfileUpdate(BaseModel):
    """
    Modelo de datos para que un usuario actualice sus datos no sensibles.
    """
    firstname: FirstnameType = None
    lastname: LastnameType = None
    dateofbirth: datetime = None
    country: CountryType = None
    city: CityType = None

    class Config:
        extra = 'forbid'

class ResetPasswordRequest(BaseModel):
    token: str 
    new_pass: PasswordType

    class Config:
        extra = 'forbid'

class ChangePasswordRequest(BaseModel):
    old_pass: PasswordType = None
    new_pass: PasswordType

    class Config:
        extra = 'forbid'
