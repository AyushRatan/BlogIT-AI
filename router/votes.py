from fastapi import APIRouter,status,HTTPException,Depends
from database import get_db
from sqlalchemy.orm import Session
from oauth2 import get_current_user
from schemas import VotePayload
import models


router = APIRouter(prefix="/votes",tags=["Votes"])


@router.post("/",status_code=status.HTTP_201_CREATED)
async def set_vote(vote:VotePayload,db:Session=Depends(get_db),current_user:models.User = Depends(get_current_user)):

    post = db.query(models.Post).filter(models.Post.id==vote.post_id).first()
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id==current_user.id)
    found_vote = vote_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id:{vote.post_id} not found")
    
    if vote.vote_dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="user already has upvoted")
        
        new_vote = models.Vote(post_id=vote.post_id,user_id=current_user.id)
        db.add(new_vote)
        db.commit()

        return {"msg":"successfully added vote"}

    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"vote does not exist")
        
        db.delete(found_vote)
        db.commit()

        return {"msg":"successfully removed vote"}
    
