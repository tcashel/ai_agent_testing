"""
Tests for SQL query generation and execution.
"""
import os
import pytest
from typing import List, Dict, Any
from langchain_community.utilities import SQLDatabase

from src.agent.sql_agent import SQLQueryAgent
from src.config.llm_config import LLMConfig, LLMProvider, OpenAISettings
from src.db.config import engine

# Mark all tests as async
pytestmark = pytest.mark.asyncio

# Ensure we have OPENAI_API_KEY for tests
if not os.getenv("OPENAI_API_KEY"):
    pytest.skip("OPENAI_API_KEY not set", allow_module_level=True)

@pytest.fixture
def agent():
    """Create a SQL agent for testing."""
    config = LLMConfig(
        provider=LLMProvider.OPENAI,
        settings=OpenAISettings(
            model_name="gpt-4-turbo-preview",
            temperature=0.0,
            api_key=os.getenv("OPENAI_API_KEY")
        )
    )
    db = SQLDatabase(engine)
    return SQLQueryAgent(config, db)

async def test_simple_query(agent: SQLQueryAgent):
    """Test a simple SELECT query."""
    results = await agent.run("List all customers")
    assert isinstance(results, list)
    assert len(results) > 0
    assert all(isinstance(row, dict) for row in results)

async def test_complex_query(agent: SQLQueryAgent):
    """Test a complex query with aggregation."""
    results = await agent.run("What is the total revenue per customer?")
    assert isinstance(results, list)
    assert len(results) > 0
    assert all(isinstance(row, dict) for row in results)
    assert "total_revenue" in results[0]

async def test_parameterized_query(agent: SQLQueryAgent):
    """Test query with parameters."""
    results = await agent.run("Find all sales after January 1st, 2024")
    assert isinstance(results, list)
    assert all(isinstance(row, dict) for row in results)
    assert all(row["date"] > "2024-01-01" for row in results)

async def test_unsafe_query_blocked(agent: SQLQueryAgent):
    """Test that unsafe queries are blocked."""
    with pytest.raises(ValueError, match="Only SELECT queries are allowed"):
        await agent.run("DELETE FROM customers") 