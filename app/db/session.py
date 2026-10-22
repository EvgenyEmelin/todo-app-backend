from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.config.config import get_settings

settings = get_settings()

engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(bind=engine,expire_on_commit=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

DbSession = Annotated[Session, Depends(get_db)]