"""
Configuration management for the application.
Combines settings from .env and config.toml files.
"""
import os
from pathlib import Path
from typing import Optional
import tomli
from dotenv import load_dotenv

from .llm_config import LLMConfig, LLMProvider

# Load environment variables from .env file
load_dotenv()

# Get project root directory (where pyproject.toml or .git is)
def find_project_root() -> Path:
    """Find the project root directory."""
    current = Path.cwd()
    while current != current.parent:
        if (current / ".git").exists() or (current / "pyproject.toml").exists():
            return current
        current = current.parent
    return current

# Load config.toml
PROJECT_ROOT = find_project_root()
CONFIG_PATH = PROJECT_ROOT / "config.toml"
with open(CONFIG_PATH, "rb") as f:
    TOML_CONFIG = tomli.load(f)

def get_llm_config() -> LLMConfig:
    """Get LLM configuration based on environment and config files.
    
    Returns:
        LLMConfig: Configuration for the language model
    """
    # Get provider from environment or fall back to config.toml
    provider = os.getenv("LLM_PROVIDER", TOML_CONFIG["llm"]["default_provider"])
    
    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required when using OpenAI")
            
        return LLMConfig.openai(
            model_name=TOML_CONFIG["llm"]["openai"]["model_name"],
            temperature=TOML_CONFIG["llm"]["openai"]["temperature"],
            api_key=api_key
        )
    
    elif provider == "ollama":
        return LLMConfig.ollama(
            model_name=TOML_CONFIG["llm"]["ollama"]["model_name"],
            temperature=TOML_CONFIG["llm"]["ollama"]["temperature"]
        )
    
    raise ValueError(f"Unsupported LLM provider: {provider}")

# Environment
APP_ENV = os.getenv("APP_ENV", "development")
IS_DEVELOPMENT = APP_ENV == "development"

# Database settings (for future use)
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "ai_query_assistant")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres") 