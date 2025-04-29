"""Template parser for managing and loading localized LLM prompt templates.

This module provides functionality to load templates from language-specific files,
substitute variables, and handle language fallbacks. It uses Python's string.Template
system for variable substitution and dynamic module imports to load templates.

Templates are organized by:
1. Language (e.g., 'en', 'ar')
2. Group (e.g., 'rag')
3. Template name (e.g., 'system_prompt')

Typical usage:
    parser = TemplateParser(language='en')
    template = parser.get('rag', 'system_prompt')
    prompt_with_vars = parser.get('rag', 'document_prompt', {'doc_num': 1, 'chunk_text': 'content'})
"""

import os
from typing import Dict, Optional, Any

class TemplateParser:
    """Parser for loading and substituting localized prompt templates.
    
    This class handles loading templates from language-specific module files,
    substituting variables, and providing fallback to a default language when
    a specific template is not available in the requested language.
    
    Attributes:
        current_path (str): The absolute path to the template parser directory.
        default_language (str): The fallback language to use if requested templates 
            are not available in the primary language.
        language (str): The currently active language for template loading.
    """

    def __init__(self, language: Optional[str]=None, default_language: str='en'):
        """Initialize the template parser with language settings.
        
        Args:
            language: The primary language to use for templates. If None or not available,
                fall back to default_language.
            default_language: The fallback language to use when templates are not 
                available in the primary language. Defaults to 'en'.
        """
        self.current_path = os.path.dirname(os.path.abspath(__file__))
        self.default_language = default_language
        self.language = None

        self.set_language(language)

    
    def set_language(self, language: Optional[str]) -> None:
        """Set the active language for template loading.
        
        If the requested language is not available or None, falls back to the default language.
        
        Args:
            language: The language code to set as active (e.g., 'en', 'ar').
                If None or not available, the default language will be used.
        """
        if not language:
            self.language = self.default_language
            return

        language_path = os.path.join(self.current_path, "locales", language)
        if os.path.exists(language_path):
            self.language = language
        else:
            self.language = self.default_language

    def get(self, group: str, key: str, vars: Optional[Dict[str, Any]]=None) -> Optional[str]:
        """Get a template with variable substitution.
        
        Loads a template from the specified group and key, then substitutes any
        variables provided. If the template isn't found in the active language,
        falls back to the default language.
        
        Args:
            group: The template group (corresponds to a Python module name, e.g., 'rag').
            key: The specific template key within the group (e.g., 'system_prompt').
            vars: A dictionary of variable names and their values to substitute in
                the template. Defaults to an empty dict if None.
        
        Returns:
            The processed template with variables substituted, or None if the
            template could not be found in either the active or default language.
        """
        if vars is None:
            vars = {}
            
        if not group or not key:
            return None
        
        group_path = os.path.join(self.current_path, "locales", self.language, f"{group}.py")
        targeted_language = self.language
        
        # Try to find the template in active language, fall back to default language if not found
        if not os.path.exists(group_path):
            group_path = os.path.join(self.current_path, "locales", self.default_language, f"{group}.py")
            targeted_language = self.default_language

        if not os.path.exists(group_path):
            return None
        
        # Dynamically import the group module based on the language
        try:
            module = __import__(f"stores.llm.templates.locales.{targeted_language}.{group}", fromlist=[group])
        except ImportError:
            return None

        if not module:
            return None
        
        # Get the template from the module and substitute variables
        try:
            key_attribute = getattr(module, key)
            return key_attribute.substitute(vars)
        except (AttributeError, KeyError):
            return None
