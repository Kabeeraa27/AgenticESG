import os
from functools import lru_cache
from typing import Iterable, List

import faiss
import numpy as np

from app.config import get_settings


class FaissVectorStore:
    def __init__(self, index_path: str, dim: int) -> None:
        self.index_path = index_path
        self.dim = dim
        self.index = self._load_or_create()

    def _load_or_create(self) -> faiss.Index:
        if os.path.exists(self.index_path):
            return faiss.read_index(self.index_path)
        return faiss.IndexFlatL2(self.dim)

    def add(self, embeddings: np.ndarray) -> List[int]:
        if embeddings.ndim != 2 or embeddings.shape[1] != self.dim:
            raise ValueError("Embeddings dimension mismatch with FAISS index")
        start_id = self.index.ntotal
        self.index.add(np.ascontiguousarray(embeddings, dtype="float32"))
        ids = list(range(start_id, start_id + embeddings.shape[0]))
        self._persist()
        return ids

    def search(self, query_embeddings: np.ndarray, k: int = 5):
        if query_embeddings.ndim != 2 or query_embeddings.shape[1] != self.dim:
            raise ValueError("Query dimension mismatch with FAISS index")
        distances, indices = self.index.search(np.ascontiguousarray(query_embeddings, dtype="float32"), k)
        return distances, indices

    def _persist(self) -> None:
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        faiss.write_index(self.index, self.index_path)


@lru_cache()
def get_vector_store(dim: int) -> FaissVectorStore:
    settings = get_settings()
    return FaissVectorStore(settings.faiss_index_path, dim)
