from typing import Generator
from sqlalchemy import create_engine  
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker  

# SQLite database file path
SQLALCHEMY_DATABASE_URL = "sqlite:///./case_assistant.db"

# connect_args={"check_same_thread": False} is required for SQLite in FastAPI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None, None]:
    """Dependency generator that yields a database session per request and closes it after."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()