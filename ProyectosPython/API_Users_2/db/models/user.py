from pydantic import BaseModel, Field, EmailStr, StringConstraints, field_validator
from datetime import datetime
from typing import Annotated
from enum import Enum
import re
from fastapi import HTTPException, status

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

# Función para validar criterios de contraseña
def validate_password(value: str):
    if len(value) < 8 or len(value) > 128:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='La contraseña debe tener entre 8 y 128 caracteres.')
    if not re.search(r'[A-Z]', value):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='La contraseña debe contener al menos una letra mayúscula.')
    if not re.search(r'\d', value):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='La contraseña debe contener al menos un número.')
    if not re.search(r'[@$!%*?&]', value):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='La contraseña debe contener al menos un carácter especial.')
    return value

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
        extra = 'forbid' # Para prevenir inyección de datos no deseados, devuelve error si hay campos que no se esperan

class User_wPass(User):
    """
    Modelo de datos para un usuario con contraseña.

    Es el modelo de usuario base, pero incluye la contraseña del usuario.
    """

    password: PasswordType

    @field_validator('password')
    def validate_password_field(cls, value):
        return validate_password(value)
    
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
    
    @field_validator('new_pass')
    def validate_password_field(cls, value):
        return validate_password(value)

    class Config:
        extra = 'forbid'

class ChangePasswordRequest(BaseModel):
    old_pass: PasswordType = None
    new_pass: PasswordType

    @field_validator('new_pass')
    def validate_password_field(cls, value):
        return validate_password(value)
    
    class Config:
        extra = 'forbid'
