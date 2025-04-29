"""Controller for processing files into text chunks for RAG.

This module provides functionality for loading files of different types,
extracting their content, and splitting them into appropriate chunks
for vectorization and retrieval in the RAG pipeline.
"""
from .BaseController import BaseController
from .ProjectController import ProjectController
import os
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyMuPDFLoader
from models import ProcessingEnum
from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass

@dataclass
class Document:
    """Represents a document or chunk of text with associated metadata.
    
    Attributes:
        page_content: The text content of the document/chunk
        metadata: Associated metadata as a dictionary
    """
    page_content: str
    metadata: dict

class ProcessController(BaseController):
    """Controller for processing uploaded files into text chunks.
    
    This controller handles loading file content using appropriate loaders based on
    file type, and splitting content into chunks of appropriate size for the RAG pipeline.
    
    Currently supports:
    - Text (.txt) files
    - PDF (.pdf) files
    
    Attributes:
        project_id: ID of the project being processed
        project_path: Path to the project directory
    """

    def __init__(self, project_id: str):
        """Initialize the ProcessController with a specific project.
        
        Args:
            project_id: The ID of the project whose files will be processed
        """
        super().__init__()

        self.project_id = project_id
        self.project_path = ProjectController().get_project_path(project_id=project_id)

    def get_file_extension(self, file_id: str) -> str:
        """Extract the file extension from a file ID.
        
        Args:
            file_id: The file identifier to extract extension from
            
        Returns:
            The file extension including the dot (e.g., '.txt', '.pdf')
        """
        return os.path.splitext(file_id)[-1]

    def get_file_loader(self, file_id: str) -> Optional[Union[TextLoader, PyMuPDFLoader]]:
        """Get the appropriate document loader for a file based on its extension.
        
        Currently supports:
        - TextLoader for .txt files
        - PyMuPDFLoader for .pdf files
        
        Args:
            file_id: The file identifier to load
            
        Returns:
            An initialized document loader appropriate for the file type,
            or None if the file doesn't exist or has an unsupported type
        """
        file_ext = self.get_file_extension(file_id=file_id)
        file_path = os.path.join(
            self.project_path,
            file_id
        )

        if not os.path.exists(file_path):
            return None

        if file_ext == ProcessingEnum.TXT.value:
            return TextLoader(file_path, encoding="utf-8")

        if file_ext == ProcessingEnum.PDF.value:
            return PyMuPDFLoader(file_path)
        
        return None

    def get_file_content(self, file_id: str) -> Optional[List[Any]]:
        """Load the content of a file using the appropriate loader.
        
        Args:
            file_id: The file identifier to load content from
            
        Returns:
            A list of document objects with content and metadata as returned by the loader,
            or None if no appropriate loader could be found
        """
        loader = self.get_file_loader(file_id=file_id)
        if loader:
            return loader.load()

        return None

    def process_file_content(self, file_content: list, file_id: str,
                            chunk_size: int=100, overlap_size: int=20) -> Optional[List[Document]]:
        """Process file content into chunks suitable for the RAG pipeline.
        
        Extracts text content from loader results and splits it into chunks
        of appropriate size.
        
        Args:
            file_content: Content loaded from a file (as returned by a document loader)
            file_id: ID of the file being processed (for reference)
            chunk_size: Target size (in characters) for each chunk (default: 100)
            overlap_size: Number of characters to overlap between chunks (default: 20)
                          (Note: Currently not used in the simple splitter implementation)
            
        Returns:
            A list of Document objects representing the chunks, or None if processing failed
        """
        file_content_texts = [
            rec.page_content
            for rec in file_content
        ]

        file_content_metadata = [
            rec.metadata
            for rec in file_content
        ]

        # chunks = text_splitter.create_documents(
        #     file_content_texts,
        #     metadatas=file_content_metadata
        # )

        chunks = self.process_simpler_splitter(
            texts=file_content_texts,
            metadatas=file_content_metadata,
            chunk_size=chunk_size,
        )

        return chunks

    def process_simpler_splitter(self, texts: List[str], metadatas: List[dict], 
                               chunk_size: int, splitter_tag: str="\n") -> List[Document]:
        """Split text into chunks using a simple line-based approach.
        
        Joins all texts into a single document, splits by the specified tag,
        and then recombines lines into chunks of the target size.
        
        Args:
            texts: List of text content to split
            metadatas: Metadata for each text (currently not used in output)
            chunk_size: Target size (in characters) for each chunk
            splitter_tag: Character sequence to split text on (default: newline)
            
        Returns:
            A list of Document objects representing the chunks
        """
        full_text = " ".join(texts)

        # split by splitter_tag
        lines = [ doc.strip() for doc in full_text.split(splitter_tag) if len(doc.strip()) > 1 ]

        chunks = []
        current_chunk = ""

        for line in lines:
            current_chunk += line + splitter_tag
            if len(current_chunk) >= chunk_size:
                chunks.append(Document(
                    page_content=current_chunk.strip(),
                    metadata={}
                ))

                current_chunk = ""

        if len(current_chunk) >= 0:
            chunks.append(Document(
                page_content=current_chunk.strip(),
                metadata={}
            ))

        return chunks


    

