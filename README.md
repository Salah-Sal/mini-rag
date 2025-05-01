# mini-rag

This is a minimal implementation of the RAG model for question answering.

> 📚 **New Developers**: If you're new to the project, check out our [Getting Started Guide](./docs/getting-started.md) to navigate the documentation.

## The Course

This is an educational project where all of the codes where explained (step by step) via a set of `Arabic` youtube videos. Please check the list:

| #   | Title                                         | Link                                                                                                 | Codes                                                        |
| --- | --------------------------------------------- | ---------------------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| 1   | About the Course ماذا ولمـــاذا               | [Video](https://www.youtube.com/watch?v=Vv6e2Rb1Q6w&list=PLvLvlVqNQGHCUR2p0b8a0QpVjDUg50wQj)         | NA                                                           |
| 2   | What will we build ماذا سنبنى في المشروع      | [Video](https://www.youtube.com/watch?v=_l5S5CdxE-Q&list=PLvLvlVqNQGHCUR2p0b8a0QpVjDUg50wQj&index=2) | NA                                                           |
| 3   | Setup your tools الأدوات الأساسية             | [Video](https://www.youtube.com/watch?v=VSFbkFRAT4w&list=PLvLvlVqNQGHCUR2p0b8a0QpVjDUg50wQj&index=3) | NA                                                           |
| 4   | Project Architecture                          | [Video](https://www.youtube.com/watch?v=Ei_nBwBbFUQ&list=PLvLvlVqNQGHCUR2p0b8a0QpVjDUg50wQj&index=4) | [branch](https://github.com/bakrianoo/mini-rag/tree/tut-001) |
| 5   | Welcome to FastAPI                            | [Video](https://www.youtube.com/watch?v=cpOuCdzN_Mo&list=PLvLvlVqNQGHCUR2p0b8a0QpVjDUg50wQj&index=5) | [branch](https://github.com/bakrianoo/mini-rag/tree/tut-002) |
| 6   | Nested Routes + Env Values                    | [Video](https://www.youtube.com/watch?v=CrR2Bz2Y7Hw&list=PLvLvlVqNQGHCUR2p0b8a0QpVjDUg50wQj&index=6) | [branch](https://github.com/bakrianoo/mini-rag/tree/tut-003) |
| 7   | Uploading a File                              | [Video](https://www.youtube.com/watch?v=5alMKCbFqWs&list=PLvLvlVqNQGHCUR2p0b8a0QpVjDUg50wQj&index=7) | [branch](https://github.com/bakrianoo/mini-rag/tree/tut-004) |
| 8   | File Processing                               | [Video](https://www.youtube.com/watch?v=gQgr2iwtSBw)                                                 | [branch](https://github.com/bakrianoo/mini-rag/tree/tut-005) |
| 9   | Docker - MongoDB - Motor                      | [Video](https://www.youtube.com/watch?v=2NOKWm0xJAk)                                                 | [branch](https://github.com/bakrianoo/mini-rag/tree/tut-006) |
| 10  | Mongo Schemes and Models                      | [Video](https://www.youtube.com/watch?v=zgcnnMJXXV8)                                                 | [branch](https://github.com/bakrianoo/mini-rag/tree/tut-007) |
| 11  | Mongo Indexing                                | [Video](https://www.youtube.com/watch?v=iO8FAmUVcjE)                                                 | [branch](https://github.com/bakrianoo/mini-rag/tree/tut-008) |
| 12  | Data Pipeline Enhancements                    | [Video](https://www.youtube.com/watch?v=4x1DuezZBDU)                                                 | [branch](https://github.com/bakrianoo/mini-rag/tree/tut-008) |
| 13  | Checkpoint-1                                  | [Video](https://www.youtube.com/watch?v=7xIsZkCisPk)                                                 | [branch](https://github.com/bakrianoo/mini-rag/tree/tut-008) |
| 14  | LLM Factory                                   | [Video](https://www.youtube.com/watch?v=5TKRIFtIQAY)                                                 | [branch](https://github.com/bakrianoo/mini-rag/tree/tut-008) |
| 15  | Vector DB Factory                             | [Video](https://www.youtube.com/watch?v=JtS9UkvF_10)                                                 | [branch](https://github.com/bakrianoo/mini-rag/tree/tut-009) |
| 16  | Semantic Search                               | [Video](https://www.youtube.com/watch?v=V3swQKokJW8)                                                 | [branch](https://github.com/bakrianoo/mini-rag/tree/tut-010) |
| 17  | Augmented Answers                             | [Video](https://www.youtube.com/watch?v=1Wx8BoM5pLU)                                                 | [branch](https://github.com/bakrianoo/mini-rag/tree/tut-011) |
| 18  | Checkpoint-1 + Fix Issues                     | [Video](https://youtu.be/6zG4Idxldvg)                                                                | [branch](https://github.com/bakrianoo/mini-rag/tree/tut-012) |
| 19  | Ollama Local LLM Server                       | [Video](https://youtu.be/-epZ1hAAtrs)                                                                | [branch](https://github.com/bakrianoo/mini-rag/tree/tut-012) |
| 20  | From Mongo to Postgres + SQLAlchemy & Alembic | [Video](https://www.youtube.com/watch?v=BVOq7Ek2Up0)                                                 | [branch](https://github.com/bakrianoo/mini-rag/tree/tut-013) |
| 21  | The way to PgVector                           | [Video](https://www.youtube.com/watch?v=g99yq5zlYAE)                                                 | [branch](https://github.com/bakrianoo/mini-rag/tree/tut-014) |

## Architecture Overview

This project implements a Retrieval-Augmented Generation (RAG) system using a FastAPI backend.

The main components reside within the `src/` directory:

- **`main.py`**: The FastAPI application entry point, initializing configurations, database connections, LLM/Vector DB clients, and routers.
- **`routes/`**: Defines the API endpoints using FastAPI routers. Handles incoming requests and calls appropriate controllers.
- **`controllers/`**: Contains the core business logic, orchestrating tasks like file processing, vector indexing, and RAG generation by interacting with models and stores.
- **`models/`**: Defines SQLAlchemy database schemas (`db_schemes/`), data access models for interacting with the database (`ProjectModel`, `AssetModel`, `ChunkModel`), and relevant Enums.
- **`stores/`**: Manages connections and interactions with external services:
  - `llm/`: Handles communication with Large Language Models (e.g., OpenAI, Cohere) for text generation and embedding. Includes a factory pattern and prompt templating.
  - `vectordb/`: Handles communication with the vector database (PostgreSQL with `pgvector`) for storing and searching embeddings. Includes a factory pattern.
- **`helpers/`**: Contains configuration loading (`config.py`) and other utility functions.
- **`utils/`**: General utility modules (e.g., `metrics.py`).
- **`assets/`**: Contains static assets, including uploaded files (under `files/`) and the Postman collection.

Significant architectural decisions and their rationale are documented in the `docs/adr/` directory. You can find the [Architecture Decision Records here](./docs/adr/).

## Technology Stack

This project utilizes a comprehensive technology stack:

### Backend
- **FastAPI**: Python web framework for building APIs
- **Uvicorn**: ASGI server for running the FastAPI application
- **SQLAlchemy**: ORM for database interactions
- **Alembic**: Database migration tool

### Databases
- **PostgreSQL with pgvector**: Primary database with vector extension for similarity search
- **Qdrant**: Alternative vector database for storing and querying embeddings

### LLM Providers
- **OpenAI**: For text generation and embeddings
- **Cohere**: Alternative LLM provider
- **Ollama**: Optional local LLM server

### Infrastructure
- **Docker & Docker Compose**: Containerization and service orchestration
- **Nginx**: Web server and reverse proxy
- **Prometheus**: Monitoring and metrics collection
- **Grafana**: Metrics visualization dashboards

### Processing & Utilities
- **PyMuPDF**: PDF processing library
- **NLTK**: Natural Language Toolkit for text processing
- **Langchain**: Framework for working with LLMs

The system follows a factory pattern design for both LLM and Vector DB providers, allowing easy switching between different implementations.

## Requirements

- Python 3.10

#### Install Dependencies

```bash
sudo apt update
sudo apt install libpq-dev gcc python3-dev
```

#### Install Python using MiniConda

1. Download and install MiniConda from [here](https://docs.anaconda.com/free/miniconda/#quick-command-line-install)
2. Create a new environment using the following command:

```bash
$ conda create -n mini-rag python=3.10
```

3. Activate the environment:

```bash
$ conda activate mini-rag
```

### (Optional) Setup you command line interface for better readability

```bash
export PS1="\[\033[01;32m\]\u@\h:\w\n\[\033[00m\]\$ "
```

### (Optional) Run Ollama Local LLM Server using Colab + Ngrok

- Check the [notebook](https://colab.research.google.com/drive/1KNi3-9KtP-k-93T3wRcmRe37mRmGhL9p?usp=sharing) + [Video](https://youtu.be/-epZ1hAAtrs)

## Installation

### Install the required packages

```bash
$ pip install -r requirements.txt
```

### Setup the environment variables

Copy the example environment file and populate it with your specific settings (e.g., API keys, database credentials):

```bash
$ cp .env.example .env
```

Make sure to set required values like `OPENAI_API_KEY`, database connection details, etc., within the `.env` file.

### Run Alembic Migration

```bash
$ alembic upgrade head
```

## Run Docker Compose Services

The project uses Docker Compose to manage external services like the PostgreSQL database.

```bash
$ cd docker
$ cp .env.example .env
```

Ensure the `docker/.env` file contains the correct credentials matching your main `.env` file for the database service.

```bash
$ cd docker
$ sudo docker compose up -d # Run services in detached mode
```

## Run the FastAPI server

From the project root directory (where the main `requirements.txt` is):

```bash
$ uvicorn src.main:app --reload --host 0.0.0.0 --port 5000
```

## POSTMAN Collection

Download the POSTMAN collection from [/assets/mini-rag-app.postman_collection.json](/assets/mini-rag-app.postman_collection.json)
