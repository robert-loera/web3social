from datetime import datetime
from pydantic import BaseModel, EmailStr, conint
from typing import Optional


class UserCreate(BaseModel):
    '''schema for creating a user'''
    email: EmailStr
    username: str
    password: str


class User(BaseModel):
    id: int


class UserOut(BaseModel):
    id: int
    username: str
    created_at: datetime
    total_posts: int
    # rep: int

    class Config:
        orm_mode = True


class Image(BaseModel):
    url: str


class PostBase(BaseModel):
    content: str
    image: Optional[str] = None
    published: bool = True


class PostCreate(PostBase):
    pass


class UserName(BaseModel):
    username: str

    class Config:
        orm_mode = True


class Post(PostBase):
    # inherits post contents from PostBase
    id: int
    created_at: datetime
    owner_id: int
    owner: UserName

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str]


class PostVote(BaseModel):
    post_id: int
    # conint allows us to specify the user can only put 1 or less than for like = 1 unlike = 0
    dir: conint(le=1)


class Comment(BaseModel):
    post_id: int
    content: str


class CommentOut(BaseModel):
    total_comments = str
    post = Post
    all_comments: str

    class Config:
        orm_mode = True


class Reputation(BaseModel):
    '''class to give/remove reputation of a user'''
    direction: conint(ge=-1, le=1)
    reason: str
    profile: str
