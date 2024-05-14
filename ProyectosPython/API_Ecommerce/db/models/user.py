from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    id: str | None = None
    username: str
    email: str
    firstname: str
    lastname: str
    dateofbirth: datetime
    country: str
    city: str
    email_verif: bool
    registered_date: datetime = None  # Deja el valor predeterminado como None

class User_wPass(User):
    password: str

