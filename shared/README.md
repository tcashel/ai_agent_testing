# Shared Components

This directory contains common utilities, models, and components that can be reused across different projects in the monorepo.

## Contents

### Utilities

- Common logging configurations
- Environment variable loaders
- Type definitions
- Test fixtures

### Observability

- OpenLit configuration helpers
- Tracing utilities
- Cost tracking

### Database

- Common database connection utilities
- Model definitions
- Migration helpers

## How to Use

To use shared components in a project:

1. Add the shared module as a development dependency in your Poetry project:
   ```toml
   [tool.poetry.dependencies]
   shared = {path = "../../shared", develop = true}
   ```

2. Import the components as needed:
   ```python
   from shared.observability import setup_openlit
   from shared.db import get_connection
   ```

3. If your project requires additional common utilities, consider adding them to this shared directory rather than duplicating code.