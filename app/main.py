from fastapi import FastAPI
from app.routers import post,user,auth,vote
from .database import engine
from app import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.routers)
app.include_router(user.routers)
app.include_router(auth.routers)
app.include_router(vote.router)