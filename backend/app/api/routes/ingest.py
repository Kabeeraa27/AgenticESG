from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.document import Chunk, Document
from app.models.schemas import ChunkResponse, IngestRequest, IngestResponse
from app.services.chunking import chunk_text
from app.services.embeddings import get_embedding_service
from app.services.vector_store import get_vector_store

router = APIRouter()


@router.post("/ingest", response_model=IngestResponse)
def ingest_text(payload: IngestRequest, db: Session = Depends(get_db)) -> IngestResponse:
    document = Document(title=payload.title, source_type=payload.source_type, framework=payload.framework)
    db.add(document)
    db.commit()
    db.refresh(document)

    chunks = chunk_text(payload.text, max_words=payload.chunk_size, overlap=payload.chunk_overlap)
    if not chunks:
        raise HTTPException(status_code=400, detail="No chunks produced from the input text.")

    embedding_service = get_embedding_service()
    embeddings = embedding_service.embed(chunks)
    vector_store = get_vector_store(embedding_service.dimension)
    embedding_ids = vector_store.add(embeddings)

    chunk_rows: list[Chunk] = []
    for idx, text in enumerate(chunks):
        chunk_row = Chunk(
            document_id=document.id,
            text=text,
            chunk_index=idx,
            embedding_id=str(embedding_ids[idx]) if embedding_ids else None,
            meta_json=None,
        )
        db.add(chunk_row)
        chunk_rows.append(chunk_row)

    db.commit()

    return IngestResponse(
        document_id=document.id,
        chunks=[
            ChunkResponse(
                chunk_id=chunk.id,
                embedding_id=chunk.embedding_id,
                chunk_index=chunk.chunk_index,
                text=chunk.text,
            )
            for chunk in chunk_rows
        ],
    )
