from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..import schemas, database, models, oauth2
from ..database import get_db
from sqlalchemy import func
from sqlalchemy.sql.functions import coalesce


router = APIRouter(
    prefix="/reputation",
    # tags allows us to group routes
    tags=['Reputation']
)


@router.post("/")
def reputation(rep: schemas.Reputation, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    # check if username passed exists
    username = db.query(models.User).filter(
        models.User.username == rep.profile
    ).first()
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")

    # if user already gave rep to user do not allow to do another
    rep_query = db.query(models.Reputation).filter(
        models.Reputation.username == current_user.username, models.Reputation.profile == rep.profile
    ).first()

    # if a duplicate exist raise error
    if (rep_query):
        # if the user already voted on that post do not allow it to vote again
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f'user {current_user.username} has already given rep to {rep.profile}')

    # if a duplicate does not exist than we rep post
    new_rep = models.Reputation(username=current_user.username, **rep.dict())
    db.add(new_rep)
    db.commit()
    db.refresh(new_rep)
    return {"message": "reputation successfuly created"}


@router.delete("/{profile}")
def delete_rep(profile: str, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # query to ensure a rep was given to the profile
    rep = db.query(models.Reputation).filter(
        models.Reputation.username == current_user.username, models.Reputation.profile == profile
    )

    # if there dne a rep given to that profile raise error
    if rep.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Rep given to {profile} does not exist")

    # if a rep does exist delete from db
    rep.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/")
def get_rep(db: Session = Depends(get_db)):
    # query to get the rep of users
    rep = db.query(
        models.User.username,
        func.sum(coalesce(models.Reputation.direction, 0)).label('total_rep')).join(models.Reputation, models.Reputation.profile == models.User.username, isouter=True).group_by(models.User.username).all()

    print(rep)

    if rep is None:
        return {"message": "user does not exist"}

    return rep


@router.get("/{username}")
def get_rep(username: str, db: Session = Depends(get_db)):
    # query to get the rep of users
    rep = db.query(
        models.User.username,
        func.sum(coalesce(models.Reputation.direction, 0)).label('total_rep')).join(models.Reputation, models.Reputation.profile == models.User.username, isouter=True).group_by(models.User.username).filter(models.User.username == username).first()

    print(rep)

    if rep is None:
        return {"message": "user does not exist"}

    return rep
