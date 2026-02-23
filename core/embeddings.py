"""Embedding generation and caching using sentence-transformers."""

import json
import os

import numpy as np
from sentence_transformers import SentenceTransformer

from core.config import CACHE_DIR, EMBEDDING_MODEL

_model = None


def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        print(f"  Loading model: {EMBEDDING_MODEL}...")
        _model = SentenceTransformer(EMBEDDING_MODEL)
    return _model


def _cache_path(name: str) -> str:
    os.makedirs(CACHE_DIR, exist_ok=True)
    return os.path.join(CACHE_DIR, f"{name}.json")


def generate_movie_embeddings(movies: list[dict]) -> dict[str, list[float]]:
    """Generate embeddings for movies. Returns {movie_id: embedding_list}."""
    path = _cache_path("movie_embeddings")
    if os.path.exists(path):
        print("  Using cached movie embeddings.")
        with open(path) as f:
            return json.load(f)

    model = get_model()
    texts = [f"{m['title']}. {m['description']}" for m in movies]
    print(texts)
    print(f"  Generating embeddings for {len(texts)} movies...")
    vectors = model.encode(texts, show_progress_bar=True, normalize_embeddings=True)
    result = {m["id"]: vec.tolist() for m, vec in zip(movies, vectors)}
    print(result)

    with open(path, "w") as f:
        json.dump(result, f)
    print(f"  Cached to {path}")
    return result


def generate_query_embedding(text: str) -> list[float]:
    """Generate a single query embedding."""
    model = get_model()
    vec = model.encode(text, normalize_embeddings=True)
    return vec.tolist()
