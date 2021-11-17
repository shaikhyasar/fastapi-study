

from fastapi.params import Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm.session import Session
from app.schemas import CreateUser, ResponseUser
from app.database import get_db
from app.models import User
from typing import List

from app.utils import hash_password

routers = APIRouter(prefix="/users",tags=['user'])


@routers.post("/",response_model=ResponseUser)
def create_user(users:CreateUser,db:Session = Depends(get_db)):

    users.password = hash_password(users.password)

    user = User(**users.dict())
    db.add(user)
    db.commit()
    db.refresh(user)

    return user

@routers.get("/",response_model=List[ResponseUser])
def get_user(db:Session = Depends(get_db)):
    users = db.query(User).order_by(User.id).all()

    return users


