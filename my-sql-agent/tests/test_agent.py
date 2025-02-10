"""
Tests for the QueryAgent class.
"""
import pytest
from typing import List
import os
from pathlib import Path

pytestmark = pytest.mark.asyncio

from src.agent.base import QueryAgent
from src.agent.query_classifier import (
    OperationType,
    QueryPlanner,
    QueryStep,
    QueryPlan
)
from src.config.llm_config import LLMConfig, LLMProvider, OpenAISettings

# Create test config
TEST_CONFIG = LLMConfig(
    provider=LLMProvider.OPENAI,
    settings=OpenAISettings(
        model_name="gpt-4-turbo-preview",
        temperature=0.0,
        api_key=os.getenv("OPENAI_API_KEY")
    )
)

# Ensure config.toml exists for tests
def setup_test_config():
    """Create a temporary config.toml for testing if one doesn't exist."""
    if not os.path.exists("config.toml"):
        config_content = """
[llm]
default_provider = "openai"

[llm.openai]
model_name = "gpt-4-turbo-preview"
temperature = 0.0

[llm.ollama]
model_name = "mistral"
temperature = 0.0
"""
        with open("config.toml", "w") as f:
            f.write(config_content)

# Test queries and expected results
TEST_QUERIES = [
    (
        "Get me all sales data from last month",
        OperationType.DATA_RETRIEVAL,
        ["date", "sales_amount"],
        1  # Expected number of operations
    ),
    (
        "What is the average revenue per customer?",
        OperationType.DATA_ANALYSIS,
        ["customer_id", "revenue"],
        2  # Should have retrieval + analysis
    ),
    (
        "Create a bar chart of monthly sales",
        OperationType.DATA_VISUALIZATION,
        ["date", "sales_amount"],
        2  # Should have retrieval + visualization
    )
]

@pytest.fixture(autouse=True)
def setup_teardown():
    """Setup and teardown for tests."""
    config_existed = os.path.exists("config.toml")
    if not config_existed:
        setup_test_config()
    yield
    # Only remove the config file if we created it
    if not config_existed and os.path.exists("config.toml"):
        os.remove("config.toml")

async def test_agent_initialization():
    """Test that the agent can be initialized."""
    agent = QueryAgent(config=TEST_CONFIG)
    assert agent.planner is not None
    assert agent.prompt is not None

async def test_basic_query():
    """Test that the agent can process a basic query."""
    agent = QueryAgent(config=TEST_CONFIG)
    response = await agent.process_query("What is 2+2?")
    assert isinstance(response, str)
    assert len(response) > 0

@pytest.mark.parametrize("query,expected_type,expected_fields,expected_ops", TEST_QUERIES)
async def test_query_planner(query: str, expected_type: OperationType, 
                           expected_fields: List[str], expected_ops: int):
    """Test the query planner with different types of queries."""
    planner = QueryPlanner(config=TEST_CONFIG)
    result = await planner.plan(query)
    
    # Test the plan result
    assert isinstance(result, QueryPlan)
    assert result.primary_operation == expected_type
    assert len(result.operations) == expected_ops
    
    # Test that required fields are present in at least one operation
    all_fields = []
    for op in result.operations:
        if op.required_fields:
            all_fields.extend(op.required_fields)
    
    for field in expected_fields:
        assert field in all_fields, f"Expected field {field} not found in operations"
    
    # Test that operations are in logical order
    if expected_ops > 1:
        # Data retrieval should always be first for multi-step operations
        assert result.operations[0].operation_type == OperationType.DATA_RETRIEVAL
        # The primary operation should be last
        assert result.operations[-1].operation_type == expected_type