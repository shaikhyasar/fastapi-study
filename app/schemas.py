from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from pydantic.errors import cls_kwargs

from pydantic.networks import EmailStr
from pydantic.types import conint
from sqlalchemy.sql.functions import user
from starlette import status

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
    owner: ResponseUser

class Token(BaseModel):
    token: str
    token_type: str
    user_id : int

class TokenData(BaseModel):
    id: Optional[str] = None

    

class CreateVote(BaseModel):
    post_id : int
    vote_dir: conint(le=1)

class ResponseVote(BaseModel):
    post_id : int
    user_id:int