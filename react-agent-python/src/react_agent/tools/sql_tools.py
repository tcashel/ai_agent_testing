"""SQL database tools for the React Agent."""
from typing import List, Dict, Any, Optional
import os
from langchain_core.tools import BaseTool
from langchain_core.language_models import BaseLanguageModel
from langchain_community.utilities import SQLDatabase
from langchain_community.tools.sql_database.tool import (
    InfoSQLDatabaseTool,
    ListSQLDatabaseTool,
    QuerySQLCheckerTool,
    QuerySQLDataBaseTool,
)
from react_agent.configuration import Configuration

def get_sql_tools(config: Optional[Configuration] = None) -> List[BaseTool]:
    """Get SQL database tools.
    
    Args:
        config: Optional configuration instance. If None, uses default configuration.
        
    Returns:
        List of SQL database tools for querying and schema inspection.
    """
    if config is None:
        config = Configuration()
        
    # Initialize database connection
    db = SQLDatabase.from_uri(config.database_uri)
    
    # Create SQL toolkit tools
    tools = [
        QuerySQLDataBaseTool(db=db),
        InfoSQLDatabaseTool(db=db),
        ListSQLDatabaseTool(db=db),
        QuerySQLCheckerTool(db=db)
    ]
    
    return tools

def create_sql_tools(db: SQLDatabase, llm: Optional[BaseLanguageModel] = None) -> List[Dict[str, Any]]:
    """Create SQL tools for the agent.
    
    Args:
        db: SQLDatabase instance
        llm: Optional language model (will create default if None)
        
    Returns:
        List of tool configurations
    """
    # Create default LLM if none provided
    if llm is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required for SQL tools")
        llm = ChatOpenAI(
            model_name="gpt-4-turbo-preview",
            temperature=0.0,
            api_key=api_key
        )
    
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    return toolkit.get_tools()

def get_sql_tools() -> List[Dict[str, Any]]:
    """Get SQL tools with database connection from environment variables."""
    db_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    db = SQLDatabase.from_uri(db_url)
    return create_sql_tools(db) 