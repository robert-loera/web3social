from typing import List, Optional
from fastapi import APIRouter, HTTPException, status, Depends
import fastapi
from .. import schemas, utils, models, oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from sqlalchemy import func

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

'''router to create a user'''


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # hash the password
    hashed_password = utils.hash(user.password)
    # replace the password with hashed password and add it to db
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    new_user.total_posts = 0
    # need to return a token
    return new_user


'''router to get a users info with specified id'''


@router.get("/{username}", response_model=schemas.UserOut)
def get_user(username: str, db: Session = Depends(get_db)):
    # query to get user
    user = db.query(models.User.id, models.User.username, models.User.created_at, func.count(models.Post.id).
                    label("total_posts")).join(
        models.Post, models.User.username == models.Post.owner_username,
        isouter=True).group_by(models.User.id).filter(models.User.username == username).first()

    # if user dne raise error
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'user {username} does not exist')

    return user


'''router to get the current logged in user'''


@router.get("me", response_model=schemas.UserOut)
async def get_current_user(current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    user = db.query(models.User.id, models.User.username, models.User.created_at, func.count(models.Post.id).
                    label("total_posts")).join(
        models.Post, models.User.username == models.Post.owner_username,
        isouter=True).group_by(models.User.id).filter(models.User.id == current_user.id).first()
    print(current_user)
    return user


'''router to get all users'''


@router.get("/", response_model=List[schemas.UserOut])
# @router.get("/")
def get_users(db: Session = Depends(get_db), limit: int = 25, search: Optional[str] = ""):
    # query all users w option of a limit
    users = db.query(models.User.id, models.User.username, models.User.created_at, func.count(models.Post.id).
                     label("total_posts")).join(
        models.Post, models.User.id == models.Post.owner_id,
        isouter=True).group_by(models.User.id).all()

    return (users)
