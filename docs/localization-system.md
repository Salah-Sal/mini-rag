# Localization System

This document describes the template localization system in the mini-rag application, which provides multilingual prompting capabilities for the LLM components.

## Overview

The mini-rag application uses a template localization system to provide prompts in multiple languages. This system is located in `src/stores/llm/templates/` and uses Python's `string.Template` for variable substitution.

## Directory Structure

```
src/stores/llm/templates/
├── locales/           # Language-specific templates
│   ├── en/            # English templates
│   │   └── rag.py     # RAG-specific templates in English
│   └── ar/            # Arabic templates
│       └── rag.py     # RAG-specific templates in Arabic
└── template_parser.py # Parser for loading and substituting templates
```

## Template Groups

Templates are organized by functional groups, such as:

- `rag`: Templates for Retrieval-Augmented Generation

Each group represents a specific domain within the application.

## Template Structure

Each template file defines template variables for specific purposes. For example, `rag.py` contains:

- `system_prompt`: Instructions for the LLM
- `document_prompt`: Format for presenting retrieved document chunks
- `footer_prompt`: Instructions for generating the answer with the user's query

Templates use Python's `string.Template` for variable substitution, with placeholders like `$variable_name`.

## Template Parser

The `TemplateParser` class in `template_parser.py` handles loading templates and performing variable substitution:

```python
class TemplateParser:
    def __init__(self, language=None, default_language='en'):
        # Initialize with language settings
        pass

    def set_language(self, language):
        # Set the active language
        pass

    def get(self, group, key, vars=None):
        # Get a template with variable substitution
        pass
```

### Key Features

- **Language Selection**: Specify primary and fallback languages
- **Language Switching**: Change language at runtime
- **Fallback Mechanism**: Use default language if a template isn't available
- **Dynamic Loading**: Import templates from language-specific modules
- **Variable Substitution**: Replace placeholders with dynamic values

## Usage Examples

### Initialization

```python
from stores.llm.templates.template_parser import TemplateParser

# Initialize with English as primary and default language
template_parser = TemplateParser(language="en", default_language="en")
```

### Getting Templates

```python
# Get a simple template
system_prompt = template_parser.get("rag", "system_prompt")

# Get a template with variable substitution
doc_prompt = template_parser.get("rag", "document_prompt", {
    "doc_num": 1,
    "chunk_text": "This is a document chunk about mini-rag."
})
```

### Switching Languages

```python
# Switch to Arabic
template_parser.set_language("ar")

# Get the same template in Arabic
system_prompt_ar = template_parser.get("rag", "system_prompt")
```

## RAG Prompt Construction

In the `NLPController`, the RAG prompt is constructed by combining multiple templates:

```python
# Get the system prompt
system_prompt = template_parser.get("rag", "system_prompt")

# Create document prompts for each retrieved chunk
documents_prompts = "\n".join([
    template_parser.get("rag", "document_prompt", {
        "doc_num": idx + 1,
        "chunk_text": doc.text
    })
    for idx, doc in enumerate(retrieved_documents)
])

# Add the footer with the query
footer_prompt = template_parser.get("rag", "footer_prompt", {
    "query": query
})

# Combine all parts
full_prompt = "\n\n".join([documents_prompts, footer_prompt])
```

## Adding New Languages

To add a new language:

1. Create a new directory in `locales/` with the language code (e.g., `fr/` for French)
2. Create template files for each group (e.g., `rag.py`)
3. Implement the same template variables as in the English version
4. Use the language code when initializing or setting the language in `TemplateParser`

Example for French (`locales/fr/rag.py`):

```python
from string import Template

system_prompt = Template("\n".join([
    "Vous êtes un assistant pour générer une réponse pour l'utilisateur.",
    "Vous recevrez un ensemble de documents associés à la requête de l'utilisateur.",
    # ... rest of the prompt in French
]))

document_prompt = Template(
    "\n".join([
        "## Document No: $doc_num",
        "### Contenu: $chunk_text",
    ])
)

footer_prompt = Template("\n".join([
    "Sur la base des documents ci-dessus uniquement, veuillez générer une réponse pour l'utilisateur.",
    "## Question:",
    "$query",
    "",
    "## Réponse:",
]))
```

## Best Practices

1. **Consistency**: Maintain the same template variables across languages
2. **Modularity**: Keep templates organized by functional groups
3. **Testing**: Test templates in all supported languages
4. **Documentation**: Add docstrings to template files explaining variables
5. **Graceful Fallback**: Ensure templates work with the fallback mechanism
