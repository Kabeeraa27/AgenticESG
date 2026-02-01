from functools import lru_cache
from typing import List

import numpy as np
from sentence_transformers import SentenceTransformer

from app.config import get_settings


class EmbeddingService:
    def __init__(self, model_name: str) -> None:
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()

    def embed(self, texts: List[str]) -> np.ndarray:
        # normalize for cosine similarity use-cases; FAISS IndexFlatL2 can also work with L2
        return self.model.encode(texts, normalize_embeddings=True, convert_to_numpy=True)


@lru_cache()
def get_embedding_service() -> EmbeddingService:
    settings = get_settings()
    return EmbeddingService(settings.model_name)
