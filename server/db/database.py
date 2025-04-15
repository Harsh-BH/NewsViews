from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import config

# Create SQLAlchemy engine with explicit parameter for PostgreSQL
engine = create_engine(
    config.DATABASE_URL, 
    pool_pre_ping=True,  # Check connections before using them
    echo=True  # Set to False in production, helpful for debugging
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
