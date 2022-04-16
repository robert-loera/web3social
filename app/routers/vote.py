from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..import schemas, database, models, oauth2

router = APIRouter(
    prefix="/vote",
    # tags allows us to group routes
    tags=['Vote']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.PostVote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    # check to make sure the post exists
    post_id = db.query(models.Post).filter(
        models.Post.id == vote.post_id
    ).first()
    if post_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")
    # check if vote already exists
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    # user upvotes a post
    if (vote.dir == 1):
        # if user already liked the post cannot re like the post
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f'user {current_user.id} has already voted on post {vote.post_id}')
        # if the user has not already liked the post than we create one
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        return {"message": "successfully upvoted"}

    else:
        # verify user has already upvoted the post
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        # if there was a vote we delete it
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "vote successfully removed"}
