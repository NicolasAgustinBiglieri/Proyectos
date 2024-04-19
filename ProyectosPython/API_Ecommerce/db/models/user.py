from pydantic import BaseModel

class User(BaseModel):
    id: str | None = None
    username: str
    email: str
    firstname: str
    lastname: str
    dateofbirth: int
    country: str
    city: str
    email_verif: bool

class User_wPass(User):
    password: str

