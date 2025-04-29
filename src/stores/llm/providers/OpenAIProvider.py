from ..LLMInterface import LLMInterface
from ..LLMEnums import OpenAIEnums
from openai import OpenAI
import logging
from typing import List, Union

class OpenAIProvider(LLMInterface):
    """LLM provider implementation using the OpenAI API.
    
    This class implements the LLMInterface for interacting with OpenAI models
    for both text generation (e.g., GPT-3.5, GPT-4) and text embedding
    (e.g., text-embedding-ada-002).
    
    Attributes:
        api_key: OpenAI API key.
        api_url: Optional base URL for OpenAI compatible APIs (e.g., local LLM servers).
        default_input_max_characters: Default max characters for input processing.
        default_generation_max_output_tokens: Default max tokens for generation output.
        default_generation_temperature: Default temperature for generation.
        generation_model_id: ID of the model used for text generation.
        embedding_model_id: ID of the model used for text embedding.
        embedding_size: Dimension of the embedding vectors.
        client: Initialized OpenAI client.
        enums: Enum values specific to the OpenAI API (e.g., roles).
        logger: Standard Python logger instance.
    """

    def __init__(self, api_key: str, api_url: str=None,
                       default_input_max_characters: int=1000,
                       default_generation_max_output_tokens: int=1000,
                       default_generation_temperature: float=0.1):
        """Initialize the OpenAIProvider.
        
        Args:
            api_key: OpenAI API key.
            api_url: Optional base URL for OpenAI compatible APIs.
            default_input_max_characters: Default max input length.
            default_generation_max_output_tokens: Default max output tokens.
            default_generation_temperature: Default generation temperature.
        """
        self.api_key = api_key
        self.api_url = api_url

        self.default_input_max_characters = default_input_max_characters
        self.default_generation_max_output_tokens = default_generation_max_output_tokens
        self.default_generation_temperature = default_generation_temperature

        self.generation_model_id = None

        self.embedding_model_id = None
        self.embedding_size = None

        self.client = OpenAI(
            api_key = self.api_key,
            base_url = self.api_url if self.api_url and len(self.api_url) else None
        )

        self.enums = OpenAIEnums
        self.logger = logging.getLogger(__name__)

    def set_generation_model(self, model_id: str):
        """Set the model ID for text generation."""
        self.generation_model_id = model_id

    def set_embedding_model(self, model_id: str, embedding_size: int):
        """Set the model ID and vector size for embedding."""
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size

    def process_text(self, text: str):
        """Truncate input text to the default maximum character limit."""
        return text[:self.default_input_max_characters].strip()

    def generate_text(self, prompt: str, chat_history: list=[], max_output_tokens: int=None,
                            temperature: float = None):
        """Generate text using the configured OpenAI chat completion model."""
        if not self.client:
            self.logger.error("OpenAI client was not set")
            return None

        if not self.generation_model_id:
            self.logger.error("Generation model for OpenAI was not set")
            return None
        
        max_output_tokens = max_output_tokens if max_output_tokens else self.default_generation_max_output_tokens
        temperature = temperature if temperature else self.default_generation_temperature

        chat_history.append(
            self.construct_prompt(prompt=prompt, role=OpenAIEnums.USER.value)
        )

        response = self.client.chat.completions.create(
            model = self.generation_model_id,
            messages = chat_history,
            max_tokens = max_output_tokens,
            temperature = temperature
        )

        if not response or not response.choices or len(response.choices) == 0 or not response.choices[0].message:
            self.logger.error("Error while generating text with OpenAI")
            return None

        return response.choices[0].message.content


    def embed_text(self, text: Union[str, List[str]], document_type: str = None):
        """Generate text embeddings using the configured OpenAI embedding model.
        
        Args:
            text: A single string or a list of strings to embed.
            document_type: Not used by OpenAI provider.
            
        Returns:
            A list of embedding vectors (list of lists of floats), or None on error.
        """
        if not self.client:
            self.logger.error("OpenAI client was not set")
            return None
        
        if isinstance(text, str):
            text = [text]

        if not self.embedding_model_id:
            self.logger.error("Embedding model for OpenAI was not set")
            return None
        
        response = self.client.embeddings.create(
            model = self.embedding_model_id,
            input = text,
        )

        if not response or not response.data or len(response.data) == 0 or not response.data[0].embedding:
            self.logger.error("Error while embedding text with OpenAI")
            return None

        return [ rec.embedding for rec in response.data ]

    def construct_prompt(self, prompt: str, role: str):
        """Construct a prompt message dictionary for the OpenAI Chat API format."""
        return {
            "role": role,
            "content": prompt,
        }
    


    

