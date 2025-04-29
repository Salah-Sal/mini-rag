# ADR-004: Template Engine for LLM Prompts

**Status:** Accepted

**Context:**

The mini-rag application needs to generate prompts for Large Language Models (LLMs) that:

1. Include dynamic content (e.g., retrieved document chunks, user queries)
2. Support multiple languages (e.g., English, Arabic)
3. Maintain a consistent structure while allowing customization
4. Are maintainable and separated from the application logic

Proper prompt engineering is critical for effective Retrieval-Augmented Generation systems, as the quality and structure of prompts directly impact the LLM's understanding and response generation. As the application evolves, prompts may need to be refined, and new language support may be added.

**Decision:**

We decided to implement a custom templating system with the following components:

1. **Python's `string.Template`** as the core templating engine for variable substitution
2. **File-based organization** with:
   - Template groups (e.g., 'rag') as Python modules
   - Language-specific directories (e.g., 'en', 'ar')
   - Named templates as variables within modules (e.g., 'system_prompt', 'document_prompt')
3. **Dynamic module loading** to retrieve templates at runtime
4. **Fallback mechanism** to use default language templates when the requested language is unavailable

**Consequences:**

_Positive:_

- **Simplicity**: `string.Template` is part of the Python standard library, requiring no external dependencies and using a straightforward `$variable_name` syntax.
- **Language Support**: The directory-based structure allows easy addition of new languages without code changes.
- **Maintainability**: Prompts are stored in separate files, making them easy to update without modifying application logic.
- **Reusability**: Templates can be reused across different parts of the application.
- **Type Safety**: Being Python modules, template files benefit from Python's type system and IDE support.
- **Iteration**: The structure supports ongoing prompt refinement based on observed LLM performance.

_Negative:_

- **Limited Features**: `string.Template` has fewer features than full-fledged template engines, lacking conditionals, loops, or filters.
- **Dynamic Import Complexity**: The dynamic module importing adds complexity and potential for runtime errors compared to static templates.
- **Module Caching**: Python's module import system caches modules, requiring special handling if templates need to be reloaded at runtime.

**Alternatives Considered:**

1. **Hardcoded Strings**: Simple but not maintainable or easily translatable.
2. **Jinja2**: More powerful template engine with conditionals and loops, but adds an external dependency and its syntax is more complex than needed for our use case.
3. **Template Files (non-Python)**: Could store templates as plain text files, but would require custom parsing and would not benefit from Python's module system.
4. **Database-stored Templates**: Would allow runtime updates but adds complexity and database dependency for a relatively static component.

The chosen approach balances simplicity, maintainability, and flexibility, prioritizing developer experience and the specific needs of multilingual LLM prompt management.
