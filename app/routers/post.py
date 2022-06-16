from ntpath import join
from typing import List, Optional
from fastapi import APIRouter, Response, status, Depends, HTTPException
from ..database import get_db
from .. import schemas, oauth2, models
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

'''route to create a post'''


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # create post with current logged in user as owner and pass post info as dict
    new_post = models.Post(owner_username=current_user.username, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


'''route to get all posts'''


@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), limit: int = 25, search: Optional[str] = ""):

    # query to get the post and number of votes
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes"), func.count(models.Post.content).label("total_posts")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).order_by(desc(models.Post.created_at)).all()

    return results


'''route to get specified post with passed id'''


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # query a specific post w the id given
    id_post = db.query(models.Post).filter(models.Post.id == id).first()

    print(id_post)

    # id exists return the post
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    # if the id dne
    if id_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {id} was not found')

    return post


'''route to get all of a specified useres posts'''


@router.get("of/{username}", response_model=List[schemas.PostOut])
def get_users_post(username: str, db: Session = Depends(get_db)):
    # query the users posts
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.owner_username == username).all()

    return post


'''route to delete a post with specified id'''


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # query to find post with matching id
    deleted_post = db.query(models.Post).filter(models.Post.id == id)

    # if post with that id DNE
    if deleted_post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} does not exist')

    # only allow user who created post to delete
    if deleted_post.first().owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    # delete the post
    deleted_post.delete(synchronize_session=False)
    db.commit()
    return {"message": f"post {id} deleted"}


'''route to update a post with specefied id'''


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # query to find post with matching id
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    # check that post exists
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {id} does not exist')

    # only allow user who created post update it
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()
    return post_query.first()
