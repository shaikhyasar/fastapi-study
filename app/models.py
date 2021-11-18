from sqlalchemy import Column,Integer,String,Boolean
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, nullable=False, primary_key = True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=True, server_default="TRUE")
    created_at = Column(TIMESTAMP(timezone=True),server_default=text("now()"))
    owner_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)

    owner = relationship("User")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer,nullable=False,primary_key=True)
    name = Column(String,nullable=True)
    email = Column(String, nullable=False,unique=True)
    password = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),server_default=text("now()"))

class Vote(Base):
    __tablename__ = "votes"

    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True,)
    post_id = Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True)


    # CREATE TABLE votes (
    #     user_id INTEGER NOT NULL,
    #     post_id INTEGER NOT NULL,
    #     PRIMARY KEY (user_id, post_id),
    #     FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE,
    #     FOREIGN KEY(post_id) REFERENCES posts (id) ON DELETE CASCADE
    #     )
