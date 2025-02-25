# MCP SQL Agent (Read-Only)

A secure, read-only implementation of SQL agents using the [Model Context Protocol (MCP)](https://github.com/modelcontextprotocol/servers) with PostgreSQL, Snowflake, and Grafana data sources.

## Overview

This project demonstrates how to use MCP to connect LLM agents with multiple data sources in a safe, read-only manner:

- Uses MCP servers for PostgreSQL, Snowflake, and Grafana connections
- Enforces strict read-only access for all data sources
- Enables agents to query databases and metrics data via unified interface
- Implements multiple layers of data access safety
- Provides Jupyter notebooks for interactive experimentation

## Prerequisites

- Docker and Docker Compose
- Python 3.9+
- PostgreSQL client (for local development)
- Snowflake account credentials

## Setup

1. Clone the repository
2. Add required credentials to the top-level `.env` file
3. Run `docker-compose up -d` to start all services
4. Open Jupyter notebook at http://localhost:8888

## Architecture

This implementation uses:

- OpenAI GPT models via LangChain for flexibility
- MCP servers for data source connections
- PostgreSQL for relational data (read-only access)
- Snowflake for data warehousing (read-only access)
- Grafana for metrics and time series data (read-only access)

## Security Layers

The implementation includes multiple layers of security to ensure read-only access:

1. **Agent-level validation**: The agent code filters queries to ensure they only contain SELECT statements
2. **Permission-based access**: Database connections use read-only users with restricted permissions
3. **Query pattern filtering**: Blocks queries containing dangerous keywords (INSERT, UPDATE, DELETE, etc.)
4. **MCP server configuration**: The MCP servers are configured to limit the scope and impact of queries
5. **Prompt guidance**: The LLM prompt explicitly instructs the model to only use read operations

## Contents

- `notebooks/`: Jupyter notebooks for interactive testing
- `src/`: Python source code for the agent implementation
- `config/`: Configuration files for MCP and databases
- `docker-compose.yml`: Service definitions