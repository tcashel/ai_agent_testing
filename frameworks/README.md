# AI Agent Frameworks

This directory contains projects organized by the AI agent framework they use.

## Available Frameworks

### LangChain

The `langchain/` directory contains projects that use the LangChain framework, which provides abstractions for working with language models, tools, and memory.

Key projects:
- SQL query generators
- RAG implementations
- Chain and agent patterns

### AutoGen

The `autogen/` directory contains projects that use Microsoft's AutoGen framework, which enables multi-agent conversation for complex tasks.

Key projects:
- Multi-agent conversational systems
- AutoGen Studio experimentations
- Tool usage examples

### React Agent (LangGraph)

The `react_agent/` directory contains implementations of the React agent pattern (Reasoning and Action) using LangGraph, a library for building stateful, multi-actor applications.

Key projects:
- Custom React agent implementations
- Graph-based state management
- Advanced tool-use patterns

## Working with Framework Projects

Each project has its own Poetry environment and README with specific instructions. To set up a project:

1. Navigate to the project directory:
   ```bash
   cd frameworks/langchain/project_name
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