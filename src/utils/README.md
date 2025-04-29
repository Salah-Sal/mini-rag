# Utilities Module

This module provides general utility functions for the mini-rag application.

## Contents

- `metrics.py` - Prometheus metrics utilities for monitoring application performance, including middleware for tracking HTTP request counts and latencies.
- `__init__.py` - Module initialization file.

## Usage

The metrics utilities can be integrated into the FastAPI application to enable Prometheus monitoring:

```python
from src.utils.metrics import setup_metrics

# Initialize FastAPI app
app = FastAPI()

# Setup metrics middleware and endpoint
setup_metrics(app)
```

This will add a middleware that tracks request metrics and exposes them at `/metrics` where Prometheus can scrape.
