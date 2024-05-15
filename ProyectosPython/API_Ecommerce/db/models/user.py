from pydantic import BaseModel, Field
from datetime import datetime

class User(BaseModel):
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
    password: str

