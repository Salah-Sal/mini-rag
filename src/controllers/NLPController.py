from .BaseController import BaseController
from models.db_schemes import Project, DataChunk
from stores.llm.LLMEnums import DocumentTypeEnum
from typing import List, Optional, Tuple, Any, Dict
import json

class NLPController(BaseController):
    """Controller for Natural Language Processing operations in the mini-rag system.
    
    This controller manages vector operations, semantic search, and the Retrieval-Augmented
    Generation (RAG) pipeline. It serves as the central orchestrator between database stored
    text chunks, vector embeddings, and LLM generation.
    
    Key responsibilities:
    1. Managing vector collections for projects
    2. Converting text chunks to embeddings and indexing them
    3. Performing semantic search based on query embeddings
    4. Orchestrating the RAG workflow (retrieve → augment → generate)
    
    Attributes:
        vectordb_client: Client for vector database operations (e.g., PGVector)
        generation_client: Client for text generation via LLM (e.g., OpenAI)
        embedding_client: Client for embedding generation (e.g., OpenAI embeddings)
        template_parser: Parser for loading and substituting prompt templates
        
    See Also:
        A sequence diagram of the RAG workflow is available at `/docs/diagrams/rag_sequence.md`
    """

    def __init__(self, vectordb_client, generation_client, 
                 embedding_client, template_parser):
        """Initialize the NLP Controller with required clients.
        
        Args:
            vectordb_client: The vector database client (implements VectorDBInterface)
            generation_client: The LLM client for text generation (implements LLMInterface)
            embedding_client: The embedding client for vector creation (implements LLMInterface)
            template_parser: The template parser for prompt management (TemplateParser)
        """
        super().__init__()

        self.vectordb_client = vectordb_client
        self.generation_client = generation_client
        self.embedding_client = embedding_client
        self.template_parser = template_parser

    def create_collection_name(self, project_id: str) -> str:
        """Create a standardized collection name for a project.
        
        Includes the embedding dimension to ensure vector compatibility.
        
        Args:
            project_id: The ID of the project
            
        Returns:
            A formatted collection name string
        """
        return f"collection_{self.vectordb_client.default_vector_size}_{project_id}".strip()
    
    async def reset_vector_db_collection(self, project: Project) -> Any:
        """Reset (delete) a project's vector collection.
        
        Args:
            project: The project whose vector collection should be reset
            
        Returns:
            The result from the vector database deletion operation
        """
        collection_name = self.create_collection_name(project_id=project.project_id)
        return await self.vectordb_client.delete_collection(collection_name=collection_name)
    
    async def get_vector_db_collection_info(self, project: Project) -> Dict:
        """Get information about a project's vector collection.
        
        Args:
            project: The project whose vector collection info is requested
            
        Returns:
            A dictionary containing collection information (e.g., vector count, dimensions)
        """
        collection_name = self.create_collection_name(project_id=project.project_id)
        collection_info = await self.vectordb_client.get_collection_info(collection_name=collection_name)

        return json.loads(
            json.dumps(collection_info, default=lambda x: x.__dict__)
        )
    
    async def index_into_vector_db(self, project: Project, chunks: List[DataChunk],
                                   chunks_ids: List[int], 
                                   do_reset: bool = False) -> bool:
        """Index text chunks into the vector database by converting them to embeddings.
        
        Args:
            project: The project these chunks belong to
            chunks: List of DataChunk objects containing text to be embedded
            chunks_ids: List of IDs for the chunks (used as record IDs in vector DB)
            do_reset: Whether to reset the collection before indexing
            
        Returns:
            True if indexing was successful, False otherwise
        """
        
        # step1: get collection name
        collection_name = self.create_collection_name(project_id=project.project_id)

        # step2: manage items
        texts = [ c.chunk_text for c in chunks ]
        metadata = [ c.chunk_metadata for c in  chunks]
        vectors = self.embedding_client.embed_text(text=texts, 
                                                  document_type=DocumentTypeEnum.DOCUMENT.value)

        # step3: create collection if not exists
        _ = await self.vectordb_client.create_collection(
            collection_name=collection_name,
            embedding_size=self.embedding_client.embedding_size,
            do_reset=do_reset,
        )

        # step4: insert into vector db
        _ = await self.vectordb_client.insert_many(
            collection_name=collection_name,
            texts=texts,
            metadata=metadata,
            vectors=vectors,
            record_ids=chunks_ids,
        )

        return True

    async def search_vector_db_collection(self, project: Project, text: str, limit: int = 10):
        """Perform semantic search on a project's vector collection.
        
        Args:
            project: The project to search in
            text: The query text to search for
            limit: Maximum number of results to return
            
        Returns:
            List of RetrievedDocument objects containing matching texts and scores,
            or False if search failed
        """

        # step1: get collection name
        query_vector = None
        collection_name = self.create_collection_name(project_id=project.project_id)

        # step2: get text embedding vector
        vectors = self.embedding_client.embed_text(text=text, 
                                                 document_type=DocumentTypeEnum.QUERY.value)

        if not vectors or len(vectors) == 0:
            return False
        
        if isinstance(vectors, list) and len(vectors) > 0:
            query_vector = vectors[0]

        if not query_vector:
            return False    

        # step3: do semantic search
        results = await self.vectordb_client.search_by_vector(
            collection_name=collection_name,
            vector=query_vector,
            limit=limit
        )

        if not results:
            return False

        return results
    
    async def answer_rag_question(self, project: Project, query: str, limit: int = 10) -> Tuple[Optional[str], Optional[str], Optional[List]]:
        """Generate an answer to a question using the RAG (Retrieval-Augmented Generation) approach.
        
        This method implements the core RAG pipeline:
        1. Retrieval: Perform semantic search to find relevant documents
        2. Augmentation: Construct a prompt combining the query with retrieved documents
        3. Generation: Send the augmented prompt to the LLM to generate an answer
        
        The method uses templates from the template_parser to structure the prompt,
        ensuring consistent prompting patterns. It follows these steps:
        
        1. Embed the query and find semantically similar text chunks
        2. Format each retrieved chunk using the document_prompt template
        3. Add a system prompt with instructions for the LLM
        4. Add a footer with the original query using the footer_prompt template
        5. Send the complete prompt to the LLM for answer generation
        
        Args:
            project: The project to search documents in
            query: The user's question text
            limit: Maximum number of relevant documents to retrieve (default: 10)
            
        Returns:
            A tuple containing:
            - answer: The generated answer text, or None if generation failed
            - full_prompt: The complete prompt sent to the LLM (for debugging/logging)
            - chat_history: The formatted chat history (including system prompt)
        
        Note:
            The quality of results depends on:
            - The relevance of documents in the vector database
            - The embedding model's ability to match semantic similarity
            - The LLM's understanding of the prompt structure
            - The prompt template design
        """
        
        answer, full_prompt, chat_history = None, None, None

        # step1: retrieve related documents
        retrieved_documents = await self.search_vector_db_collection(
            project=project,
            text=query,
            limit=limit,
        )

        if not retrieved_documents or len(retrieved_documents) == 0:
            return answer, full_prompt, chat_history
        
        # step2: Construct LLM prompt
        system_prompt = self.template_parser.get("rag", "system_prompt")

        documents_prompts = "\n".join([
            self.template_parser.get("rag", "document_prompt", {
                    "doc_num": idx + 1,
                    "chunk_text": self.generation_client.process_text(doc.text),
            })
            for idx, doc in enumerate(retrieved_documents)
        ])

        footer_prompt = self.template_parser.get("rag", "footer_prompt", {
            "query": query
        })

        # step3: Construct Generation Client Prompts
        chat_history = [
            self.generation_client.construct_prompt(
                prompt=system_prompt,
                role=self.generation_client.enums.SYSTEM.value,
            )
        ]

        full_prompt = "\n\n".join([ documents_prompts,  footer_prompt])

        # step4: Retrieve the Answer
        answer = self.generation_client.generate_text(
            prompt=full_prompt,
            chat_history=chat_history
        )

        return answer, full_prompt, chat_history

