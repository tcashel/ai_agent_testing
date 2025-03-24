# Python Project Best Practices: Lessons from Microsoft's GraphRAG

This document captures best practices for Python project configuration and management based on Microsoft's GraphRAG repository, providing a reference for implementing similar practices in other projects.

## Poetry Setup and Configuration

### Basic Project Configuration

```toml
[tool.poetry]
name = "your-project-name"
version = "1.0.0"
description = "A concise description of your project"
authors = ["Your Name <your.email@example.com>"]
license = "MIT"
readme = "README.md"
packages = [{ include = "your_package_name" }]

[tool.poetry.urls]
"Source" = "https://github.com/your-username/your-repo"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
```

### Python Version Constraints

Define a compatible range of Python versions:

```toml
[tool.poetry.dependencies]
python = ">=3.10,<3.13"
```

### Dependency Groups

Organize dependencies into logical groups:

```toml
[tool.poetry.dependencies]
# Core dependencies
pydantic = "^2.10.0"
typer = "^0.9.0"

[tool.poetry.group.dev.dependencies]
# Development dependencies
pytest = "^8.0.0"
ruff = "^0.2.0"
pyright = "^1.1.0"
```

### CLI Entrypoints

Define command-line entry points for your application:

```toml
[tool.poetry.scripts]
your-cli-name = "your_package.cli.main:app"
```

### Dynamic Versioning (Optional)

For projects using Git-based versioning:

```toml
[tool.poetry-dynamic-versioning]
enable = true
style = "pep440"
vcs = "git"

[build-system]
requires = ["poetry-core>=1.0.0", "poetry-dynamic-versioning>=1.0.0,<2.0.0"]
build-backend = "poetry_dynamic_versioning.backend"
```

## Code Quality Tools

### Ruff Configuration (Linting & Formatting)

```toml
[tool.ruff]
target-version = "py310"
extend-include = ["*.ipynb"]  # If you have Jupyter notebooks

[tool.ruff.format]
preview = true
docstring-code-format = true
docstring-code-line-length = 80

[tool.ruff.lint]
preview = true
# Select specific rule sets
select = [
    "E",    # pycodestyle errors
    "F",    # pyflakes
    "I",    # isort
    "B",    # flake8-bugbear
    "C4",   # flake8-comprehensions
    "SIM",  # flake8-simplify
    "ARG",  # flake8-unused-arguments
    "UP",   # pyupgrade
    "D",    # pydocstyle
]

# Ignore specific rules
ignore = [
    "D100",   # Missing docstring in public module
    "D104",   # Missing docstring in public package
]

# Configure rule-specific behavior per directory
[tool.ruff.lint.per-file-ignores]
"tests/*" = ["S", "D", "ANN"]  # No need for docstrings or type annotations in tests
"*.ipynb" = ["E402"]  # Allow imports not at top in notebooks

# Configure docstring style
[tool.ruff.lint.pydocstyle]
convention = "google"  # or "numpy" or "pep257"
```

### Type Checking with Pyright

```toml
[tool.pyright]
include = ["your_package", "tests"]
exclude = ["**/node_modules", "**/__pycache__"]
typeCheckingMode = "basic"  # or "strict" for more rigorous checking
```

### Task Automation with poethepoet

```toml
[tool.poe.tasks]
# Individual commands
format = "ruff format ."
lint = "ruff check ."
typecheck = "pyright"
test = "pytest tests/"
test_coverage = "coverage run -m pytest && coverage report"

# Composite tasks
[[tool.poe.tasks.check]]
sequence = ["format", "lint", "typecheck"]
ignore_fail = "return_non_zero"

[[tool.poe.tasks.ci]]
sequence = ["check", "test"]
ignore_fail = "return_non_zero"
```

## Testing Configuration

```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"  # For async tests
testpaths = ["tests"]
python_files = "test_*.py"
python_functions = "test_*"
markers = [
    "slow: marks tests as slow",
    "integration: marks tests as integration tests",
]
env_files = [".env.test"]  # If using pytest-dotenv
```

## Environment Management

### Using dotenv for Environment Variables

```toml
[tool.poetry.dependencies]
python-dotenv = "^1.0.0"
environs = "^10.0.0"  # For typed env var parsing
```

Usage example:
```python
from environs import Env

env = Env()
env.read_env()  # Read .env file

DEBUG = env.bool("DEBUG", default=False)
API_KEY = env.str("API_KEY")
```

## Document Generation

For projects that need documentation:

```toml
[tool.poetry.group.docs.dependencies]
mkdocs-material = "^9.0.0"
mkdocs-jupyter = "^0.24.0"

[tool.poe.tasks]
serve_docs = "mkdocs serve"
build_docs = "mkdocs build"
```

## CI/CD Integration Tips

1. Pin the Poetry version in your CI workflows
2. Set up matrix testing for multiple Python versions
3. Split tests (unit, integration, smoke) to improve CI efficiency
4. Cache Poetry dependencies to speed up builds
5. Enforce semantic versioning through CI checks

## Best Practices Summary

1. **Single Source of Truth**: Keep all configuration in `pyproject.toml` where possible
2. **Dependency Management**: Use Poetry's lock file for reproducible builds
3. **Code Quality**: Integrate linting, formatting, and type checking
4. **Testing**: Follow a consistent testing approach with proper isolation
5. **Task Automation**: Define common tasks to standardize workflows
6. **Documentation**: Include comprehensive documentation with examples
7. **Versioning**: Implement semantic versioning with automated tools