# Docker Configuration

This document provides details about the Docker setup in the mini-rag application, including service configuration, monitoring tools, and deployment strategies.

## Overview

The mini-rag application uses Docker Compose to manage multiple services that work together to provide a complete RAG solution. The configuration is defined in `docker/docker-compose.yml`.

## Services

### PostgreSQL with pgvector

The primary database for storing document metadata, embeddings, and application data.

- **Image**: `ankane/pgvector`
- **Purpose**: Provides relational database functionality with vector similarity search
- **Configuration**:
  - Environment variables defined in `docker/.env`
  - Persistent volumes for data storage
  - Exposed port for external connections

### Nginx

A reverse proxy that handles HTTP requests and routes them to the appropriate services.

- **Image**: Custom build from `docker/nginx/`
- **Purpose**: Serves as the entry point for all HTTP requests, provides load balancing and SSL termination
- **Configuration**:
  - Custom configuration in `docker/nginx/conf.d/`
  - Exposed ports for HTTP/HTTPS traffic
  - Connected to the application network

### Prometheus

Monitoring system that collects metrics from the application.

- **Image**: `prom/prometheus`
- **Purpose**: Collects and stores time-series data for monitoring and alerting
- **Configuration**:
  - Configuration file in `docker/prometheus/prometheus.yml`
  - Persistent volume for metrics storage
  - Exposed port for dashboard access
  - Configured targets for the mini-rag application metrics endpoint

## Network Configuration

The Docker Compose setup creates a dedicated network for all services, allowing them to communicate with each other using service names as hostnames. External services can be accessed through exposed ports.

## Environment Variables

Environment variables are managed through `.env` files:

- `docker/.env` - Contains variables for Docker Compose services
- `.env` (root) - Contains variables for the FastAPI application

These files should be configured before starting the services, using the provided `.env.example` files as templates.

## Starting Services

To start all Docker services:

```bash
cd docker
docker compose up -d
```

To start specific services:

```bash
docker compose up -d postgres prometheus
```

## Monitoring

The application exposes metrics through a Prometheus endpoint, which are collected by the Prometheus service. These metrics include:

- HTTP request counts by endpoint, method, and status
- HTTP request latency by endpoint and method

The metrics can be visualized using Grafana (not included in the default configuration) or through the Prometheus web interface.

## Production Considerations

For production deployment, consider the following additions:

1. **Data Persistence**: Configure appropriate volume mounts for all services
2. **Scaling**: Use Docker Swarm or Kubernetes for multi-node deployment
3. **Logging**: Add a centralized logging service (e.g., ELK stack)
4. **Backups**: Implement regular database backups
5. **Security**: Configure SSL certificates and secure communication
