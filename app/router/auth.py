# Different Operations for User Auth

from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import models, schemas, utils, oauth2
from ..database import get_db


router = APIRouter(
    prefix="/login",
    tags=['Authentication']
)


# C: Create login attempt
@router.post("/", response_model=schemas.Token)
def login(user_auth: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    # We use RequestForm -> we dont need to pass "dict"/"json" in Postman

    # Find user in DB
    user = db.query(models.User).filter(
        models.User.email == user_auth.username)

    if user.first() == None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Invalid Credentials')

    if not utils.verify(user_auth.password, user.first().password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Invalid Credentials')

    # Create Token
    access_token = oauth2.create_access_token(
        data={'user_id': user.first().id})

    return {"access_token": access_token, "token_type": "bearer"}
