# AI Agent Use Cases

This directory contains projects organized by their specific use case or application area.

## Available Use Cases

### SQL Agents

The `sql_agents/` directory contains projects focused on SQL query generation, database interaction, and structured data reasoning.

Key projects:
- my-sql-agent: Advanced SQL query generation with LLMs
- langchain_sql_tutorial: Basic examples of SQL generation

These agents can:
- Generate SQL from natural language
- Execute queries against databases
- Explain query results
- Debug and improve queries

### Guard Agents

The `guard_agents/` directory contains projects focused on content moderation, prompt filtering, and safety guardrails.

Key projects:
- prompt_guarding: Examples using Llama Guard and OpenAI moderation
- content_filters: Implementations of various filter techniques

These agents help:
- Detect harmful content
- Filter unsafe prompts
- Implement responsible AI practices
- Add guardrails to LLM systems

## Working with Use Case Projects

Each project has its own Poetry environment and README with specific instructions. To set up a project:

1. Navigate to the project directory:
   ```bash
   cd use_cases/sql_agents/project_name
   ```

2. Install dependencies:
   ```bash
   poetry install
   ```

3. Activate the environment:
   ```bash
   poetry shell
   ```

4. Follow the project-specific README for further instructions