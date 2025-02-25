"""SQL database tools for the React Agent."""
from typing import List, Dict, Any, Optional
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_core.language_models import BaseLanguageModel
from langchain_openai import ChatOpenAI
import os
import sys

# Import shared environment utilities
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../../..')))
from shared.utils.env import load_env

# Load environment variables from both root and local .env files
load_env()

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