"""Database connection utilities."""

import os
from typing import Optional
from urllib.parse import quote_plus

from sqlalchemy import create_engine, Engine


def get_connection(connection_str: Optional[str] = None) -> Engine:
    """
    Create a SQLAlchemy engine from a connection string.
    
    Args:
        connection_str: Database connection string (defaults to env var SQL_DB_CONNECTION)
        
    Returns:
        SQLAlchemy engine
        
    Raises:
        ValueError: If no connection string provided and SQL_DB_CONNECTION not set
    """
    db_url = connection_str or os.getenv("SQL_DB_CONNECTION")
    
    if not db_url:
        raise ValueError(
            "No database connection string provided. "
            "Set SQL_DB_CONNECTION environment variable or provide connection_str."
        )
    
    engine = create_engine(db_url)
    return engine