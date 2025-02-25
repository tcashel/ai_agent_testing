"""
Database configuration and session management.
"""
from typing import Generator
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError

from ..config.settings import (
    DB_USER,
    DB_PASSWORD,
    DB_HOST,
    DB_PORT,
    DB_NAME,
    IS_DEVELOPMENT
)

def create_database_url() -> str:
    """Create database URL from configuration."""
    return f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def create_db_engine() -> Engine:
    """Create SQLAlchemy engine instance with connection pooling."""
    database_url = create_database_url()
    return create_engine(
        database_url,
        echo=False,  # Disable SQL logging
        pool_pre_ping=True,   # Enable connection health checks
        pool_size=5,          # Connection pool size
        max_overflow=10       # Max additional connections
    )

# Create engine instance
engine = create_db_engine()

# Create session factory
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """Get database session from connection pool.
    
    Yields:
        Session: Database session
        
    Example:
        ```python
        with get_db_session() as session:
            results = session.query(Customer).all()
        ```
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise e
    finally:
        session.close() 