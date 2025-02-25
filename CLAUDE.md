# CLAUDE.md - Agent Guidelines

## Build, Test & Lint Commands
- Run tests: `python -m pytest tests/`
- Run single test: `python -m pytest tests/path/to/test_file.py::TestClass::test_method`
- Lint code: `ruff check .` or `make lint` (in react-agent-python)
- Format code: `ruff format .` or `make format` (in react-agent-python)
- Type check: `mypy .` or included in `make lint`
- Run with observability: Add `openlit.init(otlp_endpoint="http://127.0.0.1:4318")` for tracing

## Code Style Guidelines
- **Imports**: Group std lib, 3rd party, local imports with blank lines between
- **Types**: Always use type hints (`def foo(bar: str) -> List[int]:`)
- **Naming**: snake_case for variables/functions, PascalCase for classes, UPPER_CASE for constants
- **Documentation**: Google-style docstrings (required for public APIs)
- **Error Handling**: Use explicit try/except, log errors, avoid bare excepts
- **Architecture**: Follow SOLID principles, keep components modular
- **Testing**: Mock LLM calls in tests, verify agent state, test error handling
- **Dependencies**: Use Poetry or conda environments with pinned dependencies

## Framework Guidelines
- **LangChain**: Use v0.3.18+, implement callbacks, follow async patterns
- **AutoGen**: Use v0.4.5+, handle conversation errors, monitor timeouts