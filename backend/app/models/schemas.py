from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class IngestRequest(BaseModel):
    title: str = Field(..., description="Human-friendly name for the uploaded content")
    source_type: Literal["framework", "company_doc"]
    framework: Optional[str] = Field(None, description="Framework name when source_type is framework")
    text: str = Field(..., description="Raw text to chunk and embed")
    chunk_size: int = Field(500, gt=50, description="Approx word count per chunk")
    chunk_overlap: int = Field(50, ge=0, description="Word overlap between chunks")


class ChunkResponse(BaseModel):
    chunk_id: int
    embedding_id: Optional[str]
    chunk_index: int
    text: str


class IngestResponse(BaseModel):
    document_id: int
    chunks: List[ChunkResponse]


class QueryRequest(BaseModel):
    query: str = Field(..., description="Natural language query to search relevant chunks")
    k: int = Field(5, gt=0, le=50, description="Number of nearest chunks to return")


class QueryHit(BaseModel):
    rank: int
    similarity: float
    distance: float
    chunk_id: int
    embedding_id: Optional[str]
    chunk_index: int
    text: str
    document_id: int
    title: str
    source_type: str
    framework: Optional[str]


class QueryResponse(BaseModel):
    query: str
    hits: List[QueryHit]
