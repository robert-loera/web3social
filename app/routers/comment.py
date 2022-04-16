from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from ..import schemas, database, models, oauth2
from sqlalchemy import func


router = APIRouter(
    prefix="/comment",
    # tags allows us to group routes
    tags=['Comment']
)


@router.post("/")
def create_comment(comment: schemas.Comment, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # verify the post exists
    post = db.query(models.Post).filter(
        comment.post_id == models.Post.id).first()

    # if post dne raise error
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {comment.post_id} was not found')

    # if post exists add to db
    new_comment = models.Comment(
        username=current_user.username, **comment.dict())

    new_comment.post = db.query(models.Post).filter(
        new_comment.post_id == models.Post.id).first()

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    print(new_comment.post.content)

    return new_comment


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # verify comment exist
    comment = db.query(models.Comment).filter(
        models.Comment.comment_id == id)

    if comment.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'comment with id {id} does not exist')

    # only allow signed in user to delete their own comments
    if comment.first().username != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    comment.delete(synchronize_session=False)
    db.commit()
    return {"message": "comment successfully deleted"}


@router.get("/{id}")
# @router.get("/{id}", response_model=schemas.CommentOut)
def get_comments(id: int, db: Session = Depends(get_db)):
    # query to get # of comments on post w/ post id passed
    total_comments = db.query(
        models.Post, func.count(models.Comment.comment_id).label("comments")).join(models.Comment, models.Comment.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if total_comments is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {id} was not found')

    all_comments = db.query(models.Comment.content, models.Comment.comment_id, models.Comment.username).filter(
        models.Comment.post_id == id).all()

    return total_comments, all_comments
