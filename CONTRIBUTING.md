# Contributing to mini-rag

Thank you for your interest in contributing to mini-rag! This document outlines the development workflow, standards, and best practices for contributing to this project.

## Development Workflow

### Setting Up the Development Environment

1. Fork the repository on GitHub.
2. Clone your fork locally:
   ```bash
   git clone https://github.com/your-username/mini-rag.git
   cd mini-rag
   ```
3. Set up a Python 3.10 environment (using Conda is recommended, as outlined in the README).
4. Install dependencies:
   ```bash
   pip install -r src/requirements.txt
   ```
5. Set up environment variables by copying the example:
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```
6. Set up and run the Docker services:
   ```bash
   cd docker
   cp .env.example .env
   # Edit docker/.env with your settings
   sudo docker compose up -d
   ```
7. Run database migrations:
   ```bash
   alembic upgrade head
   ```

### Making Changes

1. Create a branch for your feature or bugfix:

   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/issue-description
   ```

2. Make your changes, following the coding standards outlined below.

3. Run tests to ensure your changes don't break existing functionality:

   ```bash
   # (Add test commands once a test suite is established)
   ```

4. Commit your changes with descriptive commit messages:

   ```bash
   git commit -m "feat: add new capability to X"
   ```

   Follow [Conventional Commits](https://www.conventionalcommits.org/) formatting.

5. Push your branch to your fork:

   ```bash
   git push origin feature/your-feature-name
   ```

6. Open a Pull Request against the main repository with a clear description of the changes.

## Documentation Standards

Documentation is a first-class citizen in this project. Every code change should be accompanied by appropriate documentation updates.

### Documentation as You Go

Document your code as you write it, not after. Documentation written well after code is completed tends to be less accurate and comprehensive.

### Types of Documentation

1. **Code Documentation (Docstrings):**

   - Every module, class, method, and function should have a docstring following [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) format.
   - Include parameter descriptions, return value descriptions, and exceptions raised.
   - Add type hints for all parameters and return values.

   Example:

   ```python
   def process_template(template_name: str, variables: dict) -> str:
       """Process a prompt template by substituting variables.

       Args:
           template_name: The name of the template to process.
           variables: A dictionary of variable names and their values.

       Returns:
           The processed template with variables substituted.

       Raises:
           TemplateNotFoundError: If the template could not be found.
       """
       # ...
   ```

2. **API Documentation:**

   - Use FastAPI's support for OpenAPI documentation.
   - Add clear `summary` and `description` to route decorators.
   - Add descriptions to Pydantic model fields.

   Example:

   ```python
   @router.post("/templates",
                summary="Create a new prompt template",
                description="Creates a new prompt template with the given name, content, and project ID.")
   async def create_template(template: TemplateCreate):
       # ...
   ```

3. **README Files:**

   - Module-level README.md files should explain what the module does, its components, and how it interacts with other parts of the system.
   - Include examples where appropriate.

4. **Architecture Decision Records (ADRs):**
   - Document significant technical decisions in the `docs/adr/` directory.
   - Use the format: title, status, context, decision, consequences, and alternatives considered.
   - Create a new ADR any time a significant architectural decision is made or changed.

### Updating Documentation

- When modifying code, update the relevant documentation to reflect changes.
- Documentation changes should be part of the same pull request as the code changes.
- If documentation updates become extensive, consider creating a separate branch focusing solely on documentation improvements, but ensure it's linked to the corresponding code changes.

### Documentation Review

- Pull request reviews should include verification that documentation is updated and accurate.
- Reviewers should check for clarity, completeness, and correctness of documentation.

## Coding Standards

- Follow [PEP 8](https://pep8.org/) for Python code style.
- Use meaningful variable and function names.
- Keep functions focused on a single responsibility.
- Write clear, concise comments for complex logic.
- Add type hints for function parameters and return values.
- Use asynchronous functions (`async`/`await`) for I/O operations.

## Questions?

If you have any questions about contributing, please reach out to the project maintainers.
