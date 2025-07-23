from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings


# Create SQLAlchemy engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.SQL_ECHO,  # Configurable via environment
    future=True
)

# Create SessionLocal class
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True
)

# Create Base class for models
Base = declarative_base()


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create all tables
def create_tables():
    Base.metadata.create_all(bind=engine)