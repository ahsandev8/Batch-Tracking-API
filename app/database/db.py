from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker,Session
from sqlalchemy import create_engine
from typing import Generator
from app.config.app_config import get_settings

Base = declarative_base()

settings = get_settings()

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def init_db():
    Base.metadata.create_all(bind=engine)
