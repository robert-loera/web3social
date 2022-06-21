from fastapi import APIRouter, Response, status, Depends, HTTPException
from .. import schemas, oauth2, models
from sqlalchemy.orm import Session
from ..database import get_db


router = APIRouter(
    prefix="/messages",
    tags=['Messages']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_message(message: schemas.Message, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # check if the username passed exists
    username = db.query(models.User).filter(
        models.User.username == message.receiver).first()

    if username is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")

    # create the message for db
    new_message = models.Message(
        sender=current_user.username, **message.dict())
