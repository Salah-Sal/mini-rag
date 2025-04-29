from pydantic import BaseModel, Field
from typing import Optional

class ProcessRequest(BaseModel):
    file_id: Optional[str] = Field(
        None,
        description="Specific file ID to process. If not provided, all files in the project will be processed."
    )
    chunk_size: Optional[int] = Field(
        100,
        description="Target size (in characters) for each chunk of text. Larger chunks provide more context but may reduce retrieval precision.",
        ge=10,
        le=8000
    )
    overlap_size: Optional[int] = Field(
        20,
        description="Number of characters to overlap between adjacent chunks to maintain context across chunk boundaries.",
        ge=0
    )
    do_reset: Optional[int] = Field(
        0,
        description="Whether to reset (delete) existing chunks and vector collection before processing. 0=No, 1=Yes."
    )
