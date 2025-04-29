"""Abstract interface for Language Model (LLM) operations.

This module defines the abstract base class (ABC) that all LLM providers
(e.g., OpenAI, Cohere) must implement. It standardizes operations for
text generation, embedding creation, and prompt construction.
"""
from abc import ABC, abstractmethod

class LLMInterface(ABC):
    """Abstract base class for Large Language Model (LLM) providers.
    
    This interface defines the required operations for any LLM implementation,
    providing a consistent API for text generation, embedding, and prompt handling.
    Providers must implement all abstract methods.
    """

    @abstractmethod
    def set_generation_model(self, model_id: str):
        """Set the model identifier to be used for text generation.
        
        Args:
            model_id: The specific model ID (e.g., 'gpt-3.5-turbo', 'command-r').
        """
        pass

    @abstractmethod
    def set_embedding_model(self, model_id: str, embedding_size: int):
        """Set the model identifier and vector size for text embedding.
        
        Args:
            model_id: The specific embedding model ID (e.g., 'text-embedding-ada-002').
            embedding_size: The dimensionality of the vectors produced by the model.
        """
        pass

    @abstractmethod
    def generate_text(self, prompt: str, chat_history: list=[], max_output_tokens: int=None,
                            temperature: float = None):
        """Generate text based on a given prompt and optional chat history.
        
        Args:
            prompt: The input text prompt for the LLM.
            chat_history: A list of previous messages (formatted according to provider).
            max_output_tokens: Maximum number of tokens to generate.
            temperature: Sampling temperature for generation (controls randomness).
            
        Returns:
            The generated text as a string, or None if generation failed.
        """
        pass

    @abstractmethod
    def embed_text(self, text: str, document_type: str = None):
        """Create embedding vectors for given text(s).
        
        Args:
            text: A single string or a list of strings to embed.
            document_type: Optional type hint for the text (e.g., 'query', 'document'),
                           used by some providers like Cohere.
                           
        Returns:
            A list of embedding vectors (list of lists of floats), or None if embedding failed.
        """
        pass

    @abstractmethod
    def construct_prompt(self, prompt: str, role: str):
        """Construct a formatted prompt message suitable for the provider's API.
        
        Args:
            prompt: The text content of the message.
            role: The role associated with the message (e.g., 'user', 'system', 'assistant').
            
        Returns:
            A dictionary or object representing the formatted prompt message.
        """
        pass
