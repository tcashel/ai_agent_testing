# AI Agent Testing Monorepo

A practical exploration of various AI agent frameworks and tools, focusing on observability, development patterns, and real-world implementation. This monorepo contains examples and learnings from building AI agents with different frameworks, with a particular focus on SQL query generation and database interaction.

## Repository Organization

This monorepo is organized into the following structure:

```
ai_agent_testing/
├── .env                     # Centralized environment variables
├── frameworks/              # Projects organized by AI framework
│   ├── langchain/           # LangChain examples and projects
│   ├── autogen/             # AutoGen examples and projects 
│   └── react_agent/         # React Agent pattern implementations
├── use_cases/               # Projects organized by purpose
│   ├── sql_agents/          # SQL and database interaction agents
│   └── guard_agents/        # Prompt guarding and safety implementations
├── openlit/                 # OpenLit submodule (for observability)
└── shared/                  # Common utilities and components
```

Each project maintains its own Poetry environment for dependency isolation.

## Working with this Repository

### Environment Setup

1. **Repository-wide Environment Variables**
   - A central `.env` file in the root holds common API keys and settings
   - Project-specific variables are in individual project directories

2. **Python Environment Management**
   - Each project uses Poetry for environment management
   - Install Poetry dependencies per project:
     ```bash
     cd frameworks/langchain/project_name
     poetry install
     ```

3. **Observability**
   - OpenLit is available for observability throughout the repo:
     ```bash
     docker compose -f openlit/docker-compose.yml up -d
     ```

## Featured Projects

### SQL Agents
- **use_cases/sql_agents/my-sql-agent**: Advanced SQL query generation and database interaction
- **use_cases/sql_agents/langchain_sql_tutorial**: Basic SQL generation example with LangChain

### Framework Examples
- **frameworks/react_agent/react-agent-python**: Implementation of the React agent pattern with LangGraph
- **frameworks/autogen/autogen_testing**: Examples using the AutoGen framework
- **frameworks/llamaindex/llama-cookbook**: Collection of examples and tutorials for LLama models

## Table of Contents

- [AI Agent Testing Monorepo](#ai-agent-testing-monorepo)
  - [Repository Organization](#repository-organization)
  - [Working with this Repository](#working-with-this-repository)
    - [Environment Setup](#environment-setup)
  - [Featured Projects](#featured-projects)
  - [Observability](#observability)
    - [State Management Lessons](#state-management-lessons)
  - [Frameworks Used](#frameworks-used)
    - [LangChain](#langchain)
    - [AutoGen](#autogen)
  - [Tools Used](#tools-used)
    - [OpenLit](#openlit)
    - [Poetry](#poetry)
  - [Other Notable Tools](#other-notable-tools)
    - [Agent Frameworks](#agent-frameworks)
      - [CrewAI](#crewai)
      - [DSPy](#dspy)
      - [Semantic Kernel](#semantic-kernel)
    - [Development Tools](#development-tools)
      - [Guidance](#guidance)
      - [Haystack](#haystack)
    - [Monitoring \& Observability](#monitoring--observability)
      - [LangSmith](#langsmith)
      - [Weights \& Biases](#weights--biases)
    - [Local Development](#local-development)
      - [LiteLLM](#litellm)
      - [Ollama](#ollama)

## Quick Start

```bash
# Clone the repository
git clone https://github.com/tcashel/ai_agent_testing.git

# Set up central environment file
cp .env.example .env
# Edit .env with your API keys

# Install OpenLit for observability
docker compose -f openlit/docker-compose.yml up -d

# Work with a specific project (SQL Agent)
cd use_cases/sql_agents/my-sql-agent
poetry install
poetry run python src/agent/sql_agent.py

# Or try the React agent
cd frameworks/react_agent/react-agent-python
poetry install
make dev
```

## Observability

A critical aspect of AI agent development that I found to be absolutely essential. When building autonomous agents that can choose their own tools and actions, you can quickly accumulate unnecessary API calls and excessive token usage without realizing it.

Key findings:

- Tools like [OpenLit](https://docs.openlit.io/) (free) provide crucial logging and tracing capabilities
- Proper state management is vital - incorrect implementation can lead to exponential token usage
- Each subsequent tool call should not resend the entire message history

### State Management Lessons

- Bad: Sending entire message history for each tool call
- Good: Maintaining contextual state and sending only necessary information
- Impact: Significant reduction in API costs and improved performance

## Frameworks Used

### LangChain

[LangChain](https://python.langchain.com/docs/get_started/introduction) provides powerful tools for custom agent development and specific actions. I've used it successfully to build a SQL query generation agent that interacts with PostgreSQL.

Key aspects:

- Steeper learning curve compared to other frameworks
- Requires understanding of core concepts:
  - [Workflows](https://python.langchain.com/docs/expression_language/interface)
  - [Agents](https://python.langchain.com/docs/modules/agents/)
  - [State Management](https://python.langchain.com/docs/modules/memory/)
  - [Messages](https://python.langchain.com/docs/modules/model_io/messages/)
  - [Chains](https://python.langchain.com/docs/modules/chains/)
  - [Tools](https://python.langchain.com/docs/modules/agents/tools/)
  - [Functions](https://python.langchain.com/docs/modules/model_io/output_parsers/function)

### LangGraph Studio UI

[LangGraph](https://github.com/langchain-ai/langgraph) provides excellent visualization and insights:

- Seamless integration with OpenLit for comprehensive monitoring
- Easy initial setup with provided tooling
- Customization becomes straightforward once core concepts are understood
- Access the UI at `http://localhost:3001` after running the agent

### AutoGen

[AutoGen](https://microsoft.github.io/autogen/) offers a more streamlined approach:

- Simpler agent setup with less code
- Compatible with LangChain tools
- Version compatibility note: AutoGen `0.4.5` has limited compatibility with OpenLit
- Better for rapid prototyping and simpler use cases

### AutoGen Studio UI

[AutoGen Studio](https://microsoft.github.io/autogen/docs/studio) observations:

- Great for non-technical users
- JSON configuration import/export capabilities
- Limitations:
  - Complex to translate Python code to Studio's JSON format
  - Some agent methods lack `dump_config` functionality
  - Better suited for simpler agent configurations, not production-ready
  - Docs say it is for research and development, not production
  - able to use LangChain tools

## Tools Used

### OpenLit

[OpenLit](https://docs.openlit.io/) provides excellent observability for LLM-based applications:

- **I use OpenLit in this repo** it helped me find redundant prompts to agents.
- **Open Source**: Fully open-source observability platform with self-hosting capabilities.

- **Quick Setup**: Minimal integration required, approximately 2 lines of code:

  ```python
  import openlit
  openlit.init(otlp_endpoint="http://127.0.0.1:4318")
  ```

- **Auto-Instrumentation**: Seamlessly integrates with LangChain applications.

- **Feature-Rich Observability**:

  - Detailed agent step logging for improved debugging and insights.
  - Local development support with a pre-built Docker container.
  - Ability to add tracing to agent applications for enhanced tracking.
  - Cost tracking via [pricing JSON](https://github.com/openlit/openlit/blob/main/assets/pricing.json).
  - Advanced tracing capabilities with OpenTelemetry support.
  - Prompt management with central storage and evaluation.
  - Guardrails for security and prompt injection protection.
  - Side-by-side LLM comparison with OpenGround.

- **Cons**:

  - **Self-Hosting Complexity**: Requires infrastructure setup and ongoing maintenance.
  - **Limited Documentation**: Some features lack extensive documentation or examples.
  - **Less Community Adoption**: Smaller ecosystem compared to proprietary alternatives.

- **Access**: The UI is available at `http://127.0.0.1:3000` (default credentials in the documentation).

TODO: Explore filtering and labeling for better step/agent identification.

### LangSmith

[LangSmith](https://smith.langchain.com/) provides an advanced observability, tracing, and evaluation platform tailored for LangChain applications:

- **I have not used this** - I did not use this since it is a paid product.
- **Hosted Solution**: Managed service by LangChain, with an option for enterprise self-hosting.

- **Quick Setup**: Easy integration with LangChain applications:

  ```python
  from langsmith import Client
  client = Client()
  client.log_run(...)
  ```

- **Seamless LangChain Integration**:

  - Native tracing and debugging support for chains, agents, and LLM calls.
  - Automatic instrumentation with detailed execution traces.

- **Comprehensive Evaluation & Testing**:

  - Dataset management for benchmarking LLM performance.
  - Annotation queues for human-in-the-loop evaluations.
  - Custom evaluation metrics for fine-tuning application accuracy.

- **Prompt Engineering Tools**:

  - Prompt versioning and refinement.
  - Collaboration features for shared insights and team workflows.

- **Cost and Latency Tracking**:

  - Built-in cost estimation and performance analytics.

- **Cons**:

  - **Not Open Source**: Fully managed service with limited self-hosting options.
  - **Vendor Lock-In**: Heavily tied to the LangChain ecosystem, making it harder to integrate with non-LangChain tools.
  - **Pricing Concerns**: Costs can scale quickly with large workloads.
  - **Privacy Considerations**: Requires sending potentially sensitive data to LangChain’s servers.

- **Access**: The UI is available at [smith.langchain.com](https://smith.langchain.com/), offering a centralized dashboard for trace analysis and evaluation.

### Poetry

[Poetry](https://python-poetry.org/) - Modern Python Package and/or dependency management:

- Advantages over traditional venvs:
  - CLI-driven workflow
  - Simplified dependency management
  - Easy environment rebuilding
  - Global or local venv caching
- Notes:
  - VSCode can have issues with multiple Poetry envs in workspace subdirectories
  - Some packages (e.g., onnx) may need Docker workarounds on Linux

## Other Notable Tools

While I focused on LangChain and AutoGen, there are several other frameworks and tools worth exploring.

### Agent Frameworks

#### CrewAI

[CrewAI](https://github.com/joaomdmoura/crewAI) - Role-based agent collaboration:

- Focuses on role-based agent interactions
- Great for complex, multi-step tasks
- Excellent [documentation and tutorials](https://docs.crewai.com/)
- More structured than AutoGen for multi-agent scenarios
- Docs did not make it seem as customizable as LangChain

#### DSPy

[DSPy](https://github.com/stanfordnlp/dspy) - Stanford's LLM programming framework:

- Compiler-like approach to LLM programming
- Focus on prompt optimization
- Good for building reliable LLM applications
- More academic/research-oriented

#### Semantic Kernel

[Semantic Kernel](https://github.com/microsoft/semantic-kernel) - Microsoft's AI orchestration:

- Native integrations with Azure AI
- Strong .NET/C# support
- Plugin architecture
- Good enterprise integration features

### Development Tools

#### Guidance

[Guidance](https://github.com/guidance-ai/guidance) - Structured LLM generation:

- More control over LLM outputs
- Regular expression-like syntax
- Good for templated content generation

#### Haystack

[Haystack](https://github.com/deepset-ai/haystack) - Production-ready NLP:

- Strong RAG capabilities
- Production-ready features
- Good for document Q&A
- Enterprise-focused

### Monitoring & Observability

#### LangSmith

[LangSmith](https://www.langchain.com/langsmith) - LangChain's monitoring platform:

- Deep LangChain integration
- Comprehensive tracing
- Evaluation tools
- Note: Paid service with free tier

#### Weights & Biases

[W&B](https://wandb.ai/) - ML experiment tracking:

- LLM experiment tracking
- Prompt management
- Model evaluation tools
- Popular in ML community

### Local Development

#### LiteLLM

[LiteLLM](https://github.com/BerriAI/litellm) - Unified LLM interface:

- Single interface for multiple LLM providers
- Local and cloud model support
- Good for development and testing
- Simpler than LangChain for basic LLM calls

#### Ollama

[Ollama](https://ollama.ai/) - Local LLM management:

- Easy local model management
- I've used it successfully for local model inference with agents, but it lacks the sofitication of other llm modesl, at lest the models I can run on my local machine.
- Good performance
- Simple API
- Great for development and testing

I haven't extensively tested these tools (except for Ollama).
