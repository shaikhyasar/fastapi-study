from fastapi import APIRouter,HTTPException,status
from fastapi.params import Depends
from sqlalchemy import func
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.functions import func
from starlette.responses import Response
from app.database import get_db
from app.models import Post,Vote
from app.oauth2 import get_current_user
from app.schemas import CreatePost, ResponsePost
from typing import List, Optional
routers = APIRouter(prefix="/posts",tags=["posts"])

@routers.get("/",status_code=status.HTTP_200_OK,response_model=List[ResponsePost])
def get_all(db:Session = Depends(get_db),user_id:int = Depends(get_current_user)
            ,limit:int = 0,skip:int = 0,search:Optional[str]=""):

    if limit == 0:
        post = db.query(Post,func.count(Vote.post_id).label("Votes")).join(
            Vote,Post.id == Vote.post_id,isouter=True).group_by(
            Post.id).order_by(Post.id).filter(Post.title.contains(search)).offset(skip).all()
    else:
        post = db.query(Post,func.count(Vote.post_id).label("Votes")).join(
            Vote,Post.id == Vote.post_id,isouter=True).group_by(
                Post.id).order_by(Post.id).filter(Post.title.contains(search)).limit(limit).offset(skip).all()

        

    if not post:
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

    post = db.query(Post,func.count(Vote.post_id).label("Votes")).join(
                Vote,Post.id == Vote.post_id,isouter=True).filter(Post.id == id).group_by(Post.id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with {id} is not found")
    print(post)
    return post.first()

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
