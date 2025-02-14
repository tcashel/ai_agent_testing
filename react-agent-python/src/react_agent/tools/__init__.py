"""Tools available to the agent."""
from typing import List
import os
import logging
from langchain_core.tools import BaseTool
from .sql_tools import get_sql_tools
from .search_tools import search
from langchain_experimental.tools import PythonAstREPLTool
from langchain_experimental.tools.python.tool import PythonREPLTool

from react_agent.configuration import Configuration

logger = logging.getLogger(__name__)

# Initialize empty tools list
TOOLS: List[BaseTool] = []

# Add SQL tools if database configuration is available
try:
    # Check if all required database environment variables are set
    required_db_vars = ['DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT', 'DB_NAME']
    if all(os.getenv(var) for var in required_db_vars):
        sql_tools = get_sql_tools()
        # Add SQL tools individually
        for tool in sql_tools:
            TOOLS.append(tool)
        logger.info("SQL tools loaded successfully")
        logger.info(f"Loaded SQL tools: {[tool.name for tool in sql_tools]}")
    else:
        missing_vars = [var for var in required_db_vars if not os.getenv(var)]
        logger.warning(f"SQL tools not loaded. Missing environment variables: {', '.join(missing_vars)}")
except Exception as e:
    logger.warning(f"SQL tools not loaded due to error: {str(e)}")

# Add Python REPL tools
try:
    config = Configuration()

    # Create Python REPL tools
    python_repl = PythonREPLTool()
    python_ast_repl = PythonAstREPLTool(
        timeout=config.code_execution_timeout,
        globals={"config": config},  # Pass configuration to the tool
    )
    
    # Add tools individually
    TOOLS.append(python_repl)
    TOOLS.append(python_ast_repl)

    logger.info("Code tools loaded successfully")
except Exception as e:
    logger.warning(f"Code tools not loaded due to error: {str(e)}")

# Add search tool
TOOLS.append(search)
logger.info("Search tool loaded") 