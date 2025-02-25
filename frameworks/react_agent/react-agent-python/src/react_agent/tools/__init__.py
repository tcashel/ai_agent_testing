"""Tools available to the agent."""
from typing import List, Dict, Any
import os
import logging

logger = logging.getLogger(__name__)

# Initialize empty tools list
TOOLS: List[Dict[str, Any]] = []

# Try to load SQL tools if database configuration is available
try:
    from .sql_tools import get_sql_tools
    
    # Check if all required database environment variables are set
    required_db_vars = ['DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT', 'DB_NAME']
    if all(os.getenv(var) for var in required_db_vars):
        TOOLS.extend(get_sql_tools())
        logger.info("SQL tools loaded successfully")
    else:
        missing_vars = [var for var in required_db_vars if not os.getenv(var)]
        logger.warning(f"SQL tools not loaded. Missing environment variables: {', '.join(missing_vars)}")
except ImportError as e:
    logger.warning(f"SQL tools not loaded due to import error: {str(e)}")
except Exception as e:
    logger.warning(f"SQL tools not loaded due to error: {str(e)}") 