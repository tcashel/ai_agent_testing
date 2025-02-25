"""
Tests for the MCP SQL Agent.
"""

import os
import sys
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).resolve().parents[1]
sys.path.append(str(project_root))

# Import shared environment utilities from the repo root
repo_root = Path(__file__).resolve().parents[4]
sys.path.append(str(repo_root))
from shared.utils.env import load_env

# Load environment variables
load_env()

# Import the agent
from src.mcp_agent import MCPSQLAgent


@pytest.fixture
def mock_mcp_client():
    """Mock MCP client for testing."""
    mock_client = MagicMock()
    # Set up mock query response for PostgreSQL
    mock_postgres_response = {
        'columns': ['id', 'name', 'price', 'category'],
        'rows': [
            [1, 'Laptop', 1299.99, 'Electronics'],
            [2, 'Smartphone', 699.99, 'Electronics'],
            [8, 'Office Chair', 249.99, 'Furniture']
        ]
    }
    mock_client.query.return_value = mock_postgres_response
    return mock_client


@patch('src.mcp_agent.MCPClient')
@patch('src.mcp_agent.ChatOpenAI')
def test_agent_initialization(mock_openai, mock_mcp_client_class, mock_mcp_client):
    """Test agent initialization."""
    # Set up mocks
    mock_mcp_client_class.return_value = mock_mcp_client
    mock_openai.return_value = MagicMock()
    
    # Create agent
    agent = MCPSQLAgent()
    
    # Verify initialization
    assert agent.postgres_mcp is not None
    assert agent.snowflake_mcp is not None
    assert agent.grafana_mcp is not None
    assert agent.llm is not None
    assert len(agent.tools) == 5


@patch('src.mcp_agent.MCPClient')
@patch('src.mcp_agent.ChatOpenAI')
@patch('src.mcp_agent.AgentExecutor')
def test_agent_query(mock_agent_executor, mock_openai, mock_mcp_client_class, mock_mcp_client):
    """Test agent query method."""
    # Set up mocks
    mock_mcp_client_class.return_value = mock_mcp_client
    mock_openai.return_value = MagicMock()
    
    # Mock agent executor response
    mock_executor = MagicMock()
    mock_executor.invoke.return_value = {"output": "Top 3 products by price: Laptop, Smartphone, Office Chair"}
    mock_agent_executor.return_value = mock_executor
    
    # Create agent
    agent = MCPSQLAgent()
    
    # Test query method
    result = agent.query("What are the top 3 most expensive products?")
    
    # Verify result
    assert "Top 3 products by price" in result
    mock_executor.invoke.assert_called_once()