from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.document import Chunk
from app.models.schemas import QueryHit, QueryRequest, QueryResponse
from app.services.embeddings import get_embedding_service
from app.services.vector_store import get_vector_store

router = APIRouter()


def _cosine_from_l2(distance: float) -> float:
    # embeddings are normalized; L2 distance relates to cosine similarity via: cos = 1 - (dist^2)/2
    return 1 - (distance ** 2) / 2


@router.post("/search", response_model=QueryResponse)
def semantic_search(payload: QueryRequest, db: Session = Depends(get_db)) -> QueryResponse:
    embedding_service = get_embedding_service()
    vector_store = get_vector_store(embedding_service.dimension)

    if vector_store.index.ntotal == 0:
        raise HTTPException(status_code=400, detail="Vector store is empty. Ingest documents first.")

    query_emb = embedding_service.embed([payload.query])
    distances, indices = vector_store.search(query_emb, k=payload.k)

    hits: list[QueryHit] = []
    for rank, (dist, idx) in enumerate(zip(distances[0], indices[0]), start=1):
        if idx < 0:
            continue
        chunk = db.query(Chunk).filter(Chunk.embedding_id == str(idx)).first()
        if not chunk:
            continue
        doc = chunk.document
        hits.append(
            QueryHit(
                rank=rank,
                similarity=float(_cosine_from_l2(float(dist))),
                distance=float(dist),
                chunk_id=chunk.id,
                embedding_id=chunk.embedding_id,
                chunk_index=chunk.chunk_index,
                text=chunk.text,
                document_id=chunk.document_id,
                title=doc.title if doc else "",
                source_type=doc.source_type if doc else "",
                framework=doc.framework if doc else None,
            )
        )

    if not hits:
        raise HTTPException(status_code=404, detail="No hits found.")

    return QueryResponse(query=payload.query, hits=hits)
