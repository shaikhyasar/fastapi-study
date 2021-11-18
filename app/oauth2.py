from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from fastapi.security.oauth2 import OAuth2PasswordBearer
from sqlalchemy.orm.session import Session
from app.database import get_db
from jose import jwt, JWTError
from app.schemas import TokenData
from datetime import datetime, timedelta
from fastapi import status
from app.models import User
from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_token(data:dict):
    to_encode = data.copy()

    time_diff = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode["exp"] = time_diff

    return jwt.encode(to_encode,SECRET_KEY,algorithm= ALGORITHM)

def verify_token(token:str, credential_exception):
    
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms = [ALGORITHM])
        id = payload.get("user_id")
        if id is None:
            raise credential_exception
        tokenData = TokenData(id=id)
        return tokenData
    except JWTError:
        raise credential_exception
    

def get_current_user(token:str = Depends(oauth2_scheme),db:Session = Depends(get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not Validate",
                                headers={"WWW-Authenticate":"Bearer"})
    res =  verify_token(token,credential_exception)
    user_id = db.query(User).filter(User.id == res.id).first()
    return user_id.id
    
