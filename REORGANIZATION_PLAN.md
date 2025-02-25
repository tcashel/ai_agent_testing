# Repository Reorganization Plan

This document outlines the plan for reorganizing the AI Agent Testing repository into a more structured monorepo.

## Directory Structure

```
ai_agent_testing/
├── .env                     # Centralized environment variables
├── frameworks/              # Projects organized by AI framework
│   ├── langchain/           # LangChain examples and projects
│   ├── autogen/             # AutoGen examples and projects 
│   ├── react_agent/         # React Agent pattern implementations
│   └── llamaindex/          # LlamaIndex examples and projects
├── use_cases/               # Projects organized by purpose
│   ├── sql_agents/          # SQL and database interaction agents
│   └── guard_agents/        # Prompt guarding and safety implementations
├── openlit/                 # OpenLit submodule (for observability)
└── shared/                  # Common utilities and components
```

## Project Moves

### Step 1: Frameworks Directory

1. Move `react-agent-python` to `frameworks/react_agent/react-agent-python`
2. Move `autogen_testing` to `frameworks/autogen/autogen_testing`
3. Move `llama-cookbook` to `frameworks/llamaindex/llama-cookbook`

### Step 2: Use Cases Directory

1. Move `my-sql-agent` to `use_cases/sql_agents/my-sql-agent`
2. Move `langchain_sql_tutorial` to `use_cases/sql_agents/langchain_sql_tutorial`
3. Move `prompt_guarding` to `use_cases/guard_agents/prompt_guarding`

### Step 3: Python Environment Setup

For each project:

1. Create a `pyproject.toml` file using Poetry
2. Ensure dependencies from original project are preserved
3. Add a dependency on the shared module as needed
4. Update imports to use shared utilities

### Step 4: Environment Variables

1. Create a central `.env.example` file (already done)
2. Update project-specific code to use the shared environment loader
3. Remove duplicate environment loading code

### Step 5: Documentation

1. Create/update README.md files for each project
2. Ensure each README explains:
   - Project purpose
   - How to set up the environment
   - How to run the project
   - Key components and architecture

## Migration Process

To minimize disruption, the migration should be done in the following order:

1. Create the new directory structure (already done)
2. Set up the shared module (already done)
3. Move projects one at a time, starting with the most recent/important ones
4. Update each project's environment handling and imports
5. Test each project after migration to ensure it works correctly
6. Update documentation for each project

## Commands to Execute Migration

```bash
# Move react-agent-python
mkdir -p frameworks/react_agent/react-agent-python
cp -r react-agent-python/* frameworks/react_agent/react-agent-python/
# (Create poetry config, update imports, etc.)

# Move my-sql-agent
mkdir -p use_cases/sql_agents/my-sql-agent
cp -r my-sql-agent/* use_cases/sql_agents/my-sql-agent/
# (Create poetry config, update imports, etc.)

# Continue with other projects...
```

Each project should be migrated individually, with testing between moves to ensure nothing breaks.