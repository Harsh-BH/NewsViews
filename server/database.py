from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from config import settings

Base = declarative_base()

# Create engine
engine = create_engine(settings.DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_session() -> Session:
    """
    Get a new database session
    
    Returns:
        SQLAlchemy Session object
    """
    db = SessionLocal()
    try:
        return db
    except Exception:
        db.close()
        raise
