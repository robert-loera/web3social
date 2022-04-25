from . import models
from .database import engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from.routers import vote, user, reputation, post, idea, auth, comment

# this is for the sql alchemy to create the tables in postgres
# dont need when we use alembic
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# domains that can access our api
origins = ['*']


# basically a function that is run before every request
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# allow main to access these routers
app.include_router(post.router)
app.include_router(vote.router)
app.include_router(user.router)
app.include_router(reputation.router)
app.include_router(auth.router)
app.include_router(comment.router)


@app.get("/")
async def root():
    return {"message": "Hello World my name is Robert"}
