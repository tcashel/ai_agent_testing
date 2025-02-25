"""
Test configuration and fixtures.
"""
import os
import pytest
from dotenv import load_dotenv

@pytest.fixture(autouse=True)
def setup_test_env():
    """Set up test environment variables."""
    # Load existing environment variables from .env
    load_dotenv()
    
    # Only override non-database settings for tests
    os.environ.update({
        "APP_ENV": "test",
        "LLM_PROVIDER": "openai",
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", "test-key")
    })
    
    yield 