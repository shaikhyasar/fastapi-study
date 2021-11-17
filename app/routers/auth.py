from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from pydantic.types import StrictStr
from sqlalchemy.orm.session import Session
from app.database import get_db
from app.oauth2 import create_token
from app.schemas import LoginUser, Token
from app.models import  User
from app.utils import validate_password
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

routers = APIRouter(prefix="/login",tags=['auth'])

@routers.post("/",response_model=Token)
def login(loginuser:OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    #here OAuth2PasswordRequestForm returns two values 1. username 2. Password
    # in this case, username = email(our side) and password = password(our side)
    #this credentials needs to send via form-data under body, not in row under body
    user_query = db.query(User).filter(User.email == loginuser.username).first()
    if not user_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credential")
    
    if not validate_password(loginuser.password,user_query.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credential")
    
    token = create_token({"user_id": user_query.id})
    return {"token": token, "token_type":"Bearer"}
