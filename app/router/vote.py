# Different Operations for Voting

from statistics import mode
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)


# Create Vote to the server
@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # Check for post whether exists (Same as get_post logic)
    post = db.query(models.Post).filter(models.Post.id == vote.post_id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with {id} is not found.")

    # Check for vote whether exists
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)

    # If Like:
    if vote.dir == 1:
        # If query exists, the post is already liked.
        if vote_query.first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user.id} has already voted on post {vote.post_id}")

        # Make a new vote because query doesn't exist (not exist -> can be liked)
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully added vote"}

    # If 0/dislike:
    else:
        # If query not exist, the post is not liked before.
        if not vote_query.first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="vote doesn't exist.")

        # Delete the vote because the query exists (exist -> can be unliked)
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Successfully deleted vote"}
