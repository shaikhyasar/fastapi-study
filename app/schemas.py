from datetime import datetime
from pydantic import BaseModel
from typing import Optional

from pydantic.networks import EmailStr

class CreatePost(BaseModel):
    title : str
    content : str
    published : Optional[bool] = None

    class Config:
        orm_mode = True

class ResponsePost(CreatePost):
    id : int
    created_at : datetime
    owner_id : int

class User(BaseModel):
    name : str
    email : EmailStr

    class Config:
        orm_mode = True    

class CreateUser(User):
    password : str

class ResponseUser(User):
    id : int
    created_at : datetime

class LoginUser(BaseModel):
    username:EmailStr
    password:str

class Token(BaseModel):
    token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None