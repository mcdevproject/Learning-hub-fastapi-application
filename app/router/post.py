# Different Operations for Posts

from email.policy import HTTP
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

from typing import List, Optional

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


# C: Create
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostBase, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s, %s, %s) RETURNING *""",  # %s are placeholder; RETURNING to .fetchone()
    #               (post.title, post.content, post.published))  # SQL Injection Attack if .format or f-string
    # new_post = cursor.fetchone()
    # db_connection.commit()  # .commit() is needed for create/update/delete

    # post.dict() -> **unpack the post.dict() and put it to the model

    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


# R: Read All Posts; List[] -> List of Dicts
@router.get("/", response_model=List[schemas.PostOutput])
# @router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
              limit: int = 5, skip: int = 0, search: Optional[str] = ""):

    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()

    # for current user access only: posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id)
    """SQL: select posts.*, count(votes.post_id) as vote_count from posts 
    left join votes on posts.id = votes.post_id
    group by posts.id"""

    # post with vote count
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("vote_count")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit). offset(skip)

    return posts.all()


# R: Read One Post of current user; id: path parameter
@router.get("/{id}", response_model=schemas.PostOutput)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))  {"," to avoid TypeError}
    # post = cursor.fetchone()

    # post with vote count
    post = db.query(models.Post, func.count(models.Vote.post_id).label("vote_count")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
            models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with {id} is not found.")
    else:
        return post.first()


# U: Update
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostBase, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, post.published, (str(id),)))  {"," to avoid TypeError}
    # updated_post = cursor.fetchone()
    # db_connection.commit()

    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with {id} is not found.")

    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action.")

    post.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post.first()


# D: Delete
@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id),))  {"," to avoid TypeError}
    # deleted_post = cursor.fetchone()
    # db_connection.commit()

    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with {id} is not found.")

    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action.")

    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
