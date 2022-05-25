from enum import unique
from lib2to3.pytree import Base
from sqlalchemy import TIMESTAMP, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from .database import Base


class Post(Base):
    '''table to store all posts'''
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, nullable=False)
    content = Column(String, nullable=False)
    image = Column(String, nullable=True)
    published = Column(Boolean, server_default='True',  nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    owner_username = Column(String, ForeignKey(
        "users.username", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")


class User(Base):
    __tablename__ = 'users'
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))


class Vote(Base):
    __tablename__ = "votes"
    username = Column(String, ForeignKey(
        "users.username", ondelete='CASCADE'), primary_key=True)
    post_id = Column(Integer, ForeignKey(
        "posts.id", ondelete='CASCADE'), primary_key=True)
    post_owner = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))


class Comment(Base):
    __tablename__ = "comments"

    comment_id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, ForeignKey(
        "users.username", ondelete='CASCADE'))
    post_id = Column(Integer, ForeignKey(
        "posts.id", ondelete='CASCADE'))
    post_owner = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))


class Reputation(Base):
    __tablename__ = "reputation"
    username = Column(String, ForeignKey(
        "users.username", ondelete='CASCADE'), primary_key=True)
    direction = Column(Integer, nullable=False)
    reason = Column(String, nullable=True)
    profile = Column(String, ForeignKey(
        "users.username", ondelete='CASCADE'), primary_key=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
