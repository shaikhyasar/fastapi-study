from fastapi import APIRouter,HTTPException,status
from fastapi.params import Depends
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.functions import user
from starlette.responses import Response
from app.database import get_db
from app.models import Post
from app.oauth2 import get_current_user
from app.schemas import CreatePost, ResponsePost
from typing import List
routers = APIRouter(prefix="/posts",tags=["posts"])

@routers.get("/",status_code=status.HTTP_200_OK,response_model=List[ResponsePost])
def get_all(db:Session = Depends(get_db),user_id:int = Depends(get_current_user)):

    post = db.query(Post).order_by(Post.id).all()

    if not Post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No post is there")

    return post

@routers.post("/",response_model=ResponsePost,status_code=status.HTTP_201_CREATED)
def create_user(posts:CreatePost,db:Session = Depends(get_db),user_id:int = Depends(get_current_user)):

    post = Post(owner_id = user_id,**posts.dict())
    db.add(post)
    db.commit()
    db.refresh(post)

    return post

@routers.get("/{id}",response_model=ResponsePost,status_code=status.HTTP_200_OK)
def get_single_post(id:int, db:Session = Depends(get_db),user_id:int = Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with {id} is not found")
    
    return post

@routers.put("/{id}",response_model=ResponsePost,status_code=status.HTTP_200_OK)
def update_post(id:int,users:CreatePost,db:Session = Depends(get_db),user_id:int = Depends(get_current_user)):
    post_query = db.query(Post).filter(Post.id == id)

    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Post with {id} is not found')
    
    if post_query.first().id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Could not authorize to change post")
    
    post_query.update(users,synchronize_session=False)
    db.commit()

    return post_query.first()

@routers.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session = Depends(get_db),user_id:int = Depends(get_current_user)):
    post_query = db.query(Post).filter(id == Post.id)

    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Post with {id} is not found')
        
    if post_query.first().id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Could not authorize to change post")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
