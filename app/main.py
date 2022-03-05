# FastAPI module
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import from other codes
from . import models
from .database import engine
from .config import Settings

# Router
from .router import post, user, auth, vote

# This uses for sqlalchemy to create all tables with models.py when starting up
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "https://www.google.com",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")  # Hello World!
def root():
    return {"message": "!Hello World!"}
