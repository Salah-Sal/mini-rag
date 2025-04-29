"""
Prometheus metrics utilities for monitoring application performance.

This module provides middleware and setup functions for integrating Prometheus metrics
into a FastAPI application. It tracks HTTP request counts and latencies.
"""

from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import time

# Define metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP Request Latency', ['method', 'endpoint'])


class PrometheusMiddleware(BaseHTTPMiddleware):
    """Middleware for capturing HTTP request metrics.
    
    This middleware measures request duration and counts requests by method,
    endpoint, and status code for Prometheus monitoring.
    """
    async def dispatch(self, request: Request, call_next):
        """Process requests and record metrics.
        
        Args:
            request: The incoming HTTP request
            call_next: The next middleware or route handler
            
        Returns:
            The HTTP response
        """
        start_time = time.time()

        # Process the request
        response = await call_next(request)

        # Record metrics after request is processed
        duration = time.time() - start_time
        endpoint = request.url.path

        REQUEST_LATENCY.labels(method=request.method, endpoint=endpoint).observe(duration)
        REQUEST_COUNT.labels(method=request.method, endpoint=endpoint, status=response.status_code).inc()

        return response


def setup_metrics(app: FastAPI):
    """Setup Prometheus metrics middleware and endpoint.
    
    This function adds the Prometheus middleware to the FastAPI application
    and creates a metrics endpoint that can be scraped by Prometheus.
    
    Args:
        app: The FastAPI application instance
    """
    # Add Prometheus middleware
    app.add_middleware(PrometheusMiddleware)

    @app.get("/metrics", include_in_schema=False)
    def metrics():
        """Endpoint that returns Prometheus metrics data.
        
        Returns:
            Response containing Prometheus metrics in the appropriate format
        """
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST) 