# Different Operations for Users

from hashlib import new
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


# C: Create Users
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOutput)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # Check for email already exists or not
    new_user = db.query(models.User).filter(models.User.email == user.email)

    if new_user.first() != None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"User with this email address already exists.")

    # Hash the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    # Same procedure with "Create Post"
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# R: Read User
@router.get("/{id}", response_model=schemas.UserOutput)
def get_user(id: int, db: Session = Depends(get_db)):

    # Find user based on id
    user = db.query(models.User).filter(models.User.id == id)

    if user.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with {id} is not found.")
    else:
        return user.first()
