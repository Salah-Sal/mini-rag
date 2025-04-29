# LLM Prompt Templates

This module provides a flexible, localized templating system for LLM prompts used in the mini-rag application. It supports multiple languages and template groups, allowing for structured, maintainable, and adaptable prompts.

## Purpose

The primary purpose of this module is to:

1. **Separate prompt content from application logic** - Keep prompt texts modular and maintainable
2. **Support multilingual prompting** - Easily switch between languages (e.g., English and Arabic)
3. **Enable variable substitution** - Insert dynamic content into prompts at runtime
4. **Provide structured prompt organization** - Group related prompts by functionality (e.g., "rag")

## Key Concepts

### Template Structure

Templates are organized in a hierarchical structure:

```
templates/
├── locales/           # Language-specific templates
│   ├── en/            # English templates
│   │   └── rag.py     # RAG-specific templates in English
│   └── ar/            # Arabic templates
│       └── rag.py     # RAG-specific templates in Arabic
└── template_parser.py # Parser for loading and substituting templates
```

### Template Groups

Templates are organized by functional groups (e.g., "rag" for Retrieval-Augmented Generation prompts). Each group is a Python module with named template variables.

### Template Variables

Each template group defines specific named templates as variables in the module. For example, the `rag.py` defines:

- `system_prompt` - Instructions for the LLM behavior
- `document_prompt` - Format for presenting retrieved documents
- `footer_prompt` - Instructions for generating the answer

### Variable Substitution

Templates use Python's `string.Template` for variable substitution using the `$variable_name` syntax. For example:

- `"## Document No: $doc_num"` - `$doc_num` will be replaced with a document number
- `"$query"` - `$query` will be replaced with the user's question

## Components

### TemplateParser

The core component that loads templates and performs variable substitution:

- **Initialization**: Specify default and current language
- **Language Selection**: Choose template language or fall back to default
- **Template Retrieval**: Load templates by group and name, with dynamic substitution

### Template Files

Each template file (e.g., `rag.py`) contains multiple prompt templates for a specific domain. Templates use `string.Template` for variable substitution.

## Usage Examples

### Basic Usage

```python
from stores.llm.templates.template_parser import TemplateParser

# Initialize with English as primary and default language
template_parser = TemplateParser(language="en", default_language="en")

# Get the system prompt from the 'rag' group with no variables
system_prompt = template_parser.get("rag", "system_prompt")

# Get a document prompt with variable substitution
doc_prompt = template_parser.get("rag", "document_prompt", {
    "doc_num": 1,
    "chunk_text": "This is a document chunk about mini-rag."
})

print(doc_prompt)
# Output:
# ## Document No: 1
# ### Content: This is a document chunk about mini-rag.
```

### Switching Languages

```python
# Switch to Arabic templates
template_parser.set_language("ar")

# Get the same template in Arabic
system_prompt_ar = template_parser.get("rag", "system_prompt")

# Fallback to default language if specific template not found
unknown_template = template_parser.get("nonexistent_group", "nonexistent_key")  # Returns None
```

### RAG Prompt Construction (from NLPController)

This example shows how the RAG prompt is constructed in practice:

```python
# From NLPController.answer_rag_question
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

## Adding New Templates

To add a new template group:

1. Create a new Python file in `locales/en/` (and other languages if needed)
2. Import `Template` from `string`
3. Define template variables using `Template` objects
4. Access the new templates using `template_parser.get("new_group", "template_name")`

Example new template file (`locales/en/summarization.py`):

```python
from string import Template

system_prompt = Template("You are a summarization assistant that creates concise summaries.")

document_prompt = Template("Please summarize the following text:\n$text")

footer_prompt = Template("Make sure your summary is no more than $max_words words.")
```
