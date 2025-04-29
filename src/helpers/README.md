# Helpers Module

This module contains helper utilities that support the core functionality of the mini-rag application.

## Contents

- `config.py` - Configuration management for loading and accessing application settings from environment variables.
- `__init__.py` - Module initialization file.

## Usage

The configuration helper can be used throughout the application to access environment-based settings:

```python
from src.helpers.config import get_settings

# Get application settings
settings = get_settings()

# Use settings in your code
db_connection_string = f"postgresql://{settings.POSTGRES_USERNAME}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_MAIN_DATABASE}"
```

This provides a centralized, type-safe way to access configuration throughout the application.
