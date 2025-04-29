# Getting Started with mini-rag Documentation

Welcome to the mini-rag project! This guide will help you navigate the documentation and get up to speed quickly.

## Documentation Overview

The documentation for mini-rag is organized into several categories:

1. **Project-level README** - Basic introduction and setup instructions
2. **Architecture Decision Records (ADRs)** - Key architectural decisions and their rationale
3. **Component Documentation** - Details about specific components and subsystems
4. **API Documentation** - Details about API endpoints and usage
5. **System Configuration** - Docker setup and deployment information
6. **Component READMEs** - Individual documentation for each major module

## Suggested Reading Order

As a new developer, we recommend reading the documentation in this order:

1. **Start with the basics**:

   - Read the root `README.md` for an overview of the project and setup instructions
   - Review `CONTRIBUTING.md` to understand the development workflow

2. **Understand the architecture**:

   - Read `docs/adr/005-main-application-initialization.md` to understand the application structure
   - Explore other ADRs in `docs/adr/` to understand key architectural decisions

3. **Learn about the APIs**:

   - Review `docs/api-documentation.md` for details on all endpoints

4. **Deep dive into specific components**:
   - Explore component READMEs in their respective directories
   - Read documentation for components you'll be working with

## Key Documentation Files

### Project Setup and Overview

- `README.md` - Project overview, installation, and basic usage
- `CONTRIBUTING.md` - Development workflow and contribution guidelines
- `PLAN.md` - Documentation improvement plan

### Architecture and Design

- `docs/adr/` - Architecture Decision Records
  - `001-use-fastapi-for-web-framework.md`
  - `002-use-postgresql-pgvector-for-database.md`
  - `003-use-sqlalchemy-alembic-for-orm.md`
  - `004-template-engine-for-llm-prompts.md`
  - `005-main-application-initialization.md`

### Component Documentation

- `docs/api-documentation.md` - API endpoints and usage examples
- `docs/docker-configuration.md` - Docker setup and configuration
- `docs/localization-system.md` - Template localization system
- `docs/diagrams/rag_sequence.md` - RAG sequence diagram

### Component READMEs

- `src/controllers/README.md` - Controllers that handle business logic
- `src/models/README.md` - Data models and database schemas
- `src/routes/README.md` - API routes and handlers
- `src/stores/README.md` - External service integrations
- `src/stores/llm/README.md` - LLM integration
- `src/stores/vectordb/README.md` - Vector database integration
- `src/stores/llm/templates/README.md` - Template system for LLM prompts
- `src/utils/README.md` - Utility functions
- `src/helpers/README.md` - Helper modules

## Finding Specific Information

### "How do I set up the project?"

Read the root `README.md` file, focusing on the "Requirements", "Installation", and "Run" sections.

### "What APIs are available?"

Check `docs/api-documentation.md` for a comprehensive list of endpoints.

### "How does the RAG system work?"

1. Read `docs/diagrams/rag_sequence.md` for a visual overview
2. Study `src/controllers/NLPController.py` for implementation details
3. Review `src/stores/llm/templates/README.md` for prompt templating

### "How do I add support for a new language?"

Read `docs/localization-system.md` for a detailed guide on the localization system.

### "How does the Docker setup work?"

Review `docs/docker-configuration.md` for details on the Docker configuration.

## Contributing to Documentation

If you find gaps in the documentation or want to improve it:

1. Consult `PLAN.md` to see the documentation plan
2. Follow the guidelines in `CONTRIBUTING.md`
3. Create a pull request with your changes

## Asking for Help

If you can't find the information you need:

1. Check if there might be code-level documentation (docstrings) in the relevant files
2. Ask a more senior team member for guidance
3. Consider contributing documentation for anything that's missing

Remember, good documentation makes everyone's job easier. If you learn something that's not documented, please consider adding it to help the next developer!

## Full Documentation Map

```
├── README.md                      # Project overview
├── CONTRIBUTING.md                # Contribution guidelines
├── PLAN.md                        # Documentation plan
├── docs/                          # Documentation directory
│   ├── getting-started.md         # This guide
│   ├── api-documentation.md       # API endpoints documentation
│   ├── docker-configuration.md    # Docker setup documentation
│   ├── localization-system.md     # Template system documentation
│   ├── adr/                       # Architecture Decision Records
│   │   ├── 001-use-fastapi-for-web-framework.md
│   │   ├── 002-use-postgresql-pgvector-for-database.md
│   │   ├── 003-use-sqlalchemy-alembic-for-orm.md
│   │   ├── 004-template-engine-for-llm-prompts.md
│   │   └── 005-main-application-initialization.md
│   └── diagrams/                  # Visual documentation
│       └── rag_sequence.md        # RAG flow diagram
└── src/                           # Source code directory
    ├── main.py                    # Application entry point
    ├── controllers/               # Business logic controllers
    ├── models/                    # Data models
    ├── routes/                    # API routes
    ├── stores/                    # External service integrations
    ├── utils/                     # Utility functions
    └── helpers/                   # Helper modules
```
