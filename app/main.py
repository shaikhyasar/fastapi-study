from fastapi import FastAPI
from app.routers import post,user,auth,vote
from .database import engine
from app import models
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)
origins = []

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(post.routers)
app.include_router(user.routers)
app.include_router(auth.routers)
app.include_router(vote.router)