# Schema/Model for Data Sending and Receiving (Create and update)

from os import access
from typing import Optional
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime

from app.database import Base


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOutput(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class Post(PostBase):  # Inherit PostBase
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOutput

    class Config:
        orm_mode = True


class PostOutput(BaseModel):  # New Response Model including Vote
    Post: Post
    vote_count: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int

    # 0: dislike, 1: like
    dir: conint(le=1)
