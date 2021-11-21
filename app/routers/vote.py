from re import S
from fastapi import APIRouter,Response
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from starlette import status
from app.database import get_db
from app.schemas import CreateVote,ResponseVote
from app.oauth2 import get_current_user
from app.models import Vote
from typing import List

router = APIRouter(
    prefix="/vote",tags=["votes"]
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote_post(votes:CreateVote,db:Session= Depends(get_db),user_id:int = Depends(get_current_user)):
    vote_query = db.query(Vote).filter(Vote.user_id == user_id,Vote.post_id == votes.post_id)
    vote_found = vote_query.first()
    if votes.vote_dir == 0:
        if not vote_found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return Response(content="Vote Deleted",status_code=status.HTTP_204_NO_CONTENT)
    else:
        if vote_found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Already voted")
        vote = Vote(user_id = user_id,post_id = votes.post_id)
        db.add(vote)
        db.commit()
        db.refresh(vote)
        return {"response":"Successfully voted"}


@router.get("/",status_code=status.HTTP_200_OK,response_model=List[ResponseVote])
def get_vote(db:Session = Depends(get_db),user_id:int = Depends(get_current_user)):
    vote_query = db.query(Vote).order_by(Vote.user_id).all()

    return vote_query

