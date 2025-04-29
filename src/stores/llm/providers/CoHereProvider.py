from ..LLMInterface import LLMInterface
from ..LLMEnums import CoHereEnums, DocumentTypeEnum
import cohere
import logging
from typing import List, Union

class CoHereProvider(LLMInterface):
    """LLM provider implementation using the Cohere API.
    
    This class implements the LLMInterface for interacting with Cohere models
    for text generation (e.g., Command R) and text embedding.
    It handles specific Cohere parameters like input_type for embeddings.
    
    Attributes:
        api_key: Cohere API key.
        default_input_max_characters: Default max characters for input processing.
        default_generation_max_output_tokens: Default max tokens for generation output.
        default_generation_temperature: Default temperature for generation.
        generation_model_id: ID of the model used for text generation.
        embedding_model_id: ID of the model used for text embedding.
        embedding_size: Dimension of the embedding vectors.
        client: Initialized Cohere client.
        enums: Enum values specific to the Cohere API (e.g., roles, input types).
        logger: Standard Python logger instance.
    """

    def __init__(self, api_key: str,
                       default_input_max_characters: int=1000,
                       default_generation_max_output_tokens: int=1000,
                       default_generation_temperature: float=0.1):
        """Initialize the CoHereProvider.
        
        Args:
            api_key: Cohere API key.
            default_input_max_characters: Default max input length.
            default_generation_max_output_tokens: Default max output tokens.
            default_generation_temperature: Default generation temperature.
        """
        self.api_key = api_key

        self.default_input_max_characters = default_input_max_characters
        self.default_generation_max_output_tokens = default_generation_max_output_tokens
        self.default_generation_temperature = default_generation_temperature

        self.generation_model_id = None

        self.embedding_model_id = None
        self.embedding_size = None

        self.client = cohere.Client(api_key=self.api_key)

        self.enums = CoHereEnums
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
        """Generate text using the configured Cohere chat model."""
        if not self.client:
            self.logger.error("CoHere client was not set")
            return None

        if not self.generation_model_id:
            self.logger.error("Generation model for CoHere was not set")
            return None
        
        max_output_tokens = max_output_tokens if max_output_tokens else self.default_generation_max_output_tokens
        temperature = temperature if temperature else self.default_generation_temperature

        response = self.client.chat(
            model = self.generation_model_id,
            chat_history = chat_history,
            message = self.process_text(prompt),
            temperature = temperature,
            max_tokens = max_output_tokens
        )

        if not response or not response.text:
            self.logger.error("Error while generating text with CoHere")
            return None
        
        return response.text
    
    def embed_text(self, text: Union[str, List[str]], document_type: str = None):
        """Generate text embeddings using the configured Cohere embedding model.
        
        Uses the document_type hint to set Cohere's input_type parameter.
        
        Args:
            text: A single string or a list of strings to embed.
            document_type: Type hint for the text ('QUERY' or 'DOCUMENT').
            
        Returns:
            A list of embedding vectors (list of lists of floats), or None on error.
        """
        if not self.client:
            self.logger.error("CoHere client was not set")
            return None
        
        if isinstance(text, str):
            text = [text]
        
        if not self.embedding_model_id:
            self.logger.error("Embedding model for CoHere was not set")
            return None
        
        input_type = CoHereEnums.DOCUMENT
        if document_type == DocumentTypeEnum.QUERY:
            input_type = CoHereEnums.QUERY

        response = self.client.embed(
            model = self.embedding_model_id,
            texts = [ self.process_text(t) for t in text ],
            input_type = input_type,
            embedding_types=['float'],
        )

        if not response or not response.embeddings or not response.embeddings.float:
            self.logger.error("Error while embedding text with CoHere")
            return None
        
        return [ f for f in response.embeddings.float ]
    
    def construct_prompt(self, prompt: str, role: str):
        """Construct a prompt message dictionary for the Cohere Chat API format."""
        return {
            "role": role,
            "text": prompt,
        }