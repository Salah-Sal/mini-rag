from pydantic import BaseModel, Field
from typing import Optional

class PushRequest(BaseModel):
    do_reset: Optional[int] = Field(
        0,
        description="Whether to reset the vector collection before indexing. 0=No, 1=Yes."
    )

class SearchRequest(BaseModel):
    text: str = Field(
        ...,
        description="The search query or question to answer. For RAG, this should be a natural language question."
    )
    limit: Optional[int] = Field(
        5,
        description="Maximum number of results to return or consider. Typically 3-10 documents are used for RAG.",
        ge=1,
        le=50
    )
