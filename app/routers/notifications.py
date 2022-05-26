from fastapi import Response, status, HTTPException, Depends, APIRouter
import sqlalchemy
from sqlalchemy.orm import Session
from ..import schemas, database, models, oauth2
from ..database import get_db
from sqlalchemy import func
from sqlalchemy.sql.functions import coalesce

router = APIRouter(
    prefix="/notifications",
    # tags allows us to group routes
    tags=['Notifications']
)


@router.get("/")
def notification(db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    # query notifications of currently logged in user
    query1 = db.query(models.Reputation.type, models.Reputation.username,
                      models.Reputation.direction,  models.Reputation.profile, sqlalchemy.null().label('post_id'), sqlalchemy.null().label('content'), models.Reputation.created_at).filter(current_user.username == models.Reputation.profile)

    query2 = db.query(models.Vote.type, models.Vote.username, sqlalchemy.null(
    ), models.Vote.post_owner, models.Vote.post_id, sqlalchemy.null(), models.Vote.created_at).filter(current_user.username == models.Vote.post_owner)

    query3 = db.query(models.Comment.type, models.Comment.username, sqlalchemy.null(
    ), models.Comment.post_owner, models.Comment.post_id, models.Comment.content, models.Comment.created_at).filter(current_user.username == models.Comment.post_owner)

    query = query1.union(query2, query3).all()

    print(query)
    return query
