# MCP SQL Agent

An implementation of SQL agents using the [Model Context Protocol (MCP)](https://github.com/modelcontextprotocol/servers) with PostgreSQL, Snowflake, and Grafana data sources.

## Overview

This project demonstrates how to use MCP to connect LLM agents with multiple data sources:

- Uses MCP servers for PostgreSQL, Snowflake, and Grafana connections
- Enables agents to query databases and metrics data via unified interface
- Implements all services using Docker Compose
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
- PostgreSQL for relational data
- Snowflake for data warehousing
- Grafana for metrics and time series data

## Contents

- `notebooks/`: Jupyter notebooks for interactive testing
- `src/`: Python source code for the agent implementation
- `config/`: Configuration files for MCP and databases
- `docker-compose.yml`: Service definitions