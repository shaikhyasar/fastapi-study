from sqlalchemy.orm.session import Session, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
DATABASE_URL = "postgresql://postgres:yasar@localhost/fastapi"

engine = create_engine(DATABASE_URL)
sessionLocal = sessionmaker(bind=engine,autocommit=False,autoflush=False)

Base = declarative_base()

def get_db():
    db = sessionLocal()

    try:
        yield db
    finally:
        db.close()