"""
MCP SQL Agent Implementation

This module provides a LangChain-based agent that can query multiple data sources
using the Model Context Protocol (MCP).
"""

import os
import sys
import json
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path

# Import shared environment utilities from the repo root
repo_root = Path(__file__).resolve().parents[4]
sys.path.append(str(repo_root))
from shared.utils.env import load_env

# Load environment variables
load_env()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Import MCP and LangChain components
from mcp.client import MCPClient
import pandas as pd
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.tools import BaseTool, StructuredTool
from langchain.agents import AgentExecutor, create_openai_tools_agent


class MCPSQLAgent:
    """Agent for querying multiple data sources via MCP."""

    def __init__(
        self,
        postgres_mcp_url: str = "http://mcp-postgres:8080",
        snowflake_mcp_url: str = "http://mcp-snowflake:8080",
        grafana_mcp_url: str = "http://mcp-grafana:8080",
        model_name: str = "gpt-4",
        temperature: float = 0,
    ):
        """
        Initialize the MCP SQL Agent.

        Args:
            postgres_mcp_url: URL for PostgreSQL MCP server
            snowflake_mcp_url: URL for Snowflake MCP server
            grafana_mcp_url: URL for Grafana MCP server
            model_name: OpenAI model name to use
            temperature: Temperature for LLM generation
        """
        # Connect to MCP servers
        self.postgres_mcp = MCPClient(postgres_mcp_url)
        self.snowflake_mcp = MCPClient(snowflake_mcp_url)
        self.grafana_mcp = MCPClient(grafana_mcp_url)

        # Initialize LLM
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            api_key=os.environ.get("OPENAI_API_KEY"),
        )

        # Create tools
        self.tools = self._create_tools()

        # Create agent
        self.agent_executor = self._create_agent()

    def _create_tools(self) -> List[BaseTool]:
        """Create tools for the agent to use."""
        # PostgreSQL query tool with read-only enforcement
        def query_postgres(query: str) -> str:
            """Execute a read-only SQL query against PostgreSQL and return the results."""
            # Enforce read-only by checking for dangerous commands
            query = query.strip().lower()
            dangerous_commands = ["insert", "update", "delete", "drop", "alter", "create", "truncate", "grant", "revoke"]
            if any(cmd in query.lower() for cmd in dangerous_commands):
                return "Error: Only SELECT queries are allowed for safety reasons."
            
            # Only allow queries that start with SELECT
            if not query.startswith("select"):
                return "Error: Only SELECT queries are allowed. Please rewrite your query."
                
            try:
                response = self.postgres_mcp.query(query)
                df = pd.DataFrame(response['rows'], columns=response['columns'])
                return df.to_markdown()
            except Exception as e:
                return f"Error querying PostgreSQL: {str(e)}"

        postgres_tool = StructuredTool.from_function(
            func=query_postgres,
            name="query_postgres",
            description="Execute read-only SQL queries against PostgreSQL database with e-commerce data (only SELECT queries allowed)"
        )

        # PostgreSQL schema info tool
        def get_postgres_schema() -> str:
            """Get the schema information for PostgreSQL database."""
            try:
                schema_query = """
                SELECT 
                    table_name, 
                    column_name, 
                    data_type, 
                    is_nullable 
                FROM information_schema.columns 
                WHERE table_schema = 'public' 
                ORDER BY table_name, ordinal_position;
                """
                response = self.postgres_mcp.query(schema_query)
                df = pd.DataFrame(response['rows'], columns=response['columns'])
                return df.to_markdown()
            except Exception as e:
                return f"Error getting PostgreSQL schema: {str(e)}"

        postgres_schema_tool = StructuredTool.from_function(
            func=get_postgres_schema,
            name="get_postgres_schema",
            description="Get schema information for PostgreSQL database tables and columns"
        )

        # Snowflake query tool with read-only enforcement
        def query_snowflake(query: str) -> str:
            """Execute a read-only SQL query against Snowflake and return the results."""
            # Enforce read-only by checking for dangerous commands
            query = query.strip().lower()
            dangerous_commands = ["insert", "update", "delete", "drop", "alter", "create", "truncate", "grant", "revoke"]
            if any(cmd in query.lower() for cmd in dangerous_commands):
                return "Error: Only SELECT queries are allowed for safety reasons."
            
            # Only allow queries that start with SELECT
            if not query.startswith("select"):
                return "Error: Only SELECT queries are allowed. Please rewrite your query."
                
            try:
                response = self.snowflake_mcp.query(query)
                df = pd.DataFrame(response['rows'], columns=response['columns'])
                return df.to_markdown()
            except Exception as e:
                return f"Error querying Snowflake: {str(e)}"

        snowflake_tool = StructuredTool.from_function(
            func=query_snowflake,
            name="query_snowflake",
            description="Execute read-only SQL queries against Snowflake data warehouse (only SELECT queries allowed)"
        )

        # Grafana metrics query tool with safety checks
        def query_grafana_metrics(datasource: str, query: str, start: str, end: str, step: int = 60) -> str:
            """Query Grafana for metrics data (read-only)."""
            # Basic safety checks for the query
            if ";" in query or "delete" in query.lower() or "write" in query.lower() or "create" in query.lower():
                return "Error: The query contains potentially unsafe operations. Only read operations are allowed."
                
            try:
                # Limit step size to prevent excessive resource usage
                if step < 10:
                    step = 10  # Minimum step of 10 seconds
                if step > 3600:
                    step = 3600  # Maximum step of 1 hour
                
                response = self.grafana_mcp.query_metrics(
                    datasource=datasource, query=query, start=start, end=end, step=step
                )
                return json.dumps(response, indent=2)
            except Exception as e:
                return f"Error querying Grafana metrics: {str(e)}"

        grafana_metrics_tool = StructuredTool.from_function(
            func=query_grafana_metrics,
            name="query_grafana_metrics",
            description="Query Grafana for metrics data using PromQL or Flux queries (read-only access)"
        )

        # Grafana dashboards list tool
        def get_grafana_dashboards() -> str:
            """Get a list of available Grafana dashboards."""
            try:
                response = self.grafana_mcp.get_dashboards()
                return json.dumps(response, indent=2)
            except Exception as e:
                return f"Error getting Grafana dashboards: {str(e)}"

        grafana_dashboards_tool = StructuredTool.from_function(
            func=get_grafana_dashboards,
            name="get_grafana_dashboards",
            description="Get a list of available Grafana dashboards"
        )

        # Return all tools
        return [
            postgres_tool,
            postgres_schema_tool,
            snowflake_tool,
            grafana_metrics_tool,
            grafana_dashboards_tool,
        ]

    def _create_agent(self) -> AgentExecutor:
        """Create the LangChain agent."""
        # Define prompt template with strong read-only emphasis
        prompt = ChatPromptTemplate.from_template("""
        You are an expert SQL and data analytics agent that can query multiple data sources 
        including PostgreSQL, Snowflake, and Grafana.

        IMPORTANT: You can ONLY execute READ-ONLY operations on all data sources. Write operations are strictly prohibited.
        Only use SELECT statements for SQL databases and read-only API calls for other data sources.
        
        PostgreSQL contains e-commerce data with tables for users, products, orders, and order_items.

        Always first check the schema of the database before running queries to understand 
        the available tables and columns.

        When analyzing data, provide insights and explanations about the results, not just raw data.

        For time-series data from Grafana, consider adding visualizations where appropriate.

        If you're unsure which data source to use, ask for clarification.

        Remember: You are accessing production databases, so you must NEVER attempt to modify data in any way.
        Only execute queries that read data, never write, update, or delete.

        User's question: {input}
        """)

        # Create agent
        agent = create_openai_tools_agent(self.llm, self.tools, prompt)

        # Create and return agent executor
        return AgentExecutor(agent=agent, tools=self.tools, verbose=True)

    def query(self, question: str) -> str:
        """
        Query the agent with a question.

        Args:
            question: The question to ask the agent

        Returns:
            The agent's response as a string
        """
        logger.info(f"Querying agent with: {question}")
        response = self.agent_executor.invoke({"input": question})
        return response["output"]


# Example usage
if __name__ == "__main__":
    # Create an instance of the agent
    agent = MCPSQLAgent()

    # Define a test question
    test_question = "What are the top 3 most expensive products in our inventory?"

    # Query the agent
    result = agent.query(test_question)
    print(f"\nAgent response:\n{result}")