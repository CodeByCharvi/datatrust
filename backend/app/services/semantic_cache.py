import faiss
import numpy as np
from fastembed import TextEmbedding

MODEL_NAME = "BAAI/bge-small-en-v1.5"
DIMS = 384
THRESHOLD = 0.90


class SemanticCache:
    def __init__(self, threshold: float = THRESHOLD):
        self.threshold = threshold
        self._model = None
        self._index = faiss.IndexFlatIP(DIMS)  # inner product = cosine on normalized vectors
        self._entries = []

    def _embed(self, text: str):
        if self._model is None:
            self._model = TextEmbedding(MODEL_NAME)
        vec = np.array(list(self._model.embed([text]))[0], dtype="float32")
        vec /= np.linalg.norm(vec)
        return vec.reshape(1, -1)

    def best_match(self, question: str):
        """Return (similarity score, matched past question) or (0.0, None)."""
        if not self._entries:
            return 0.0, None
        scores, ids = self._index.search(self._embed(question), 1)
        idx = int(ids[0][0])
        if idx < 0:
            return 0.0, None
        return float(scores[0][0]), self._entries[idx]["question"]

    def get(self, question: str):
        """Return a cached result only if the match is close enough."""
        if not self._entries:
            return None
        scores, ids = self._index.search(self._embed(question), 1)
        score, idx = float(scores[0][0]), int(ids[0][0])
        if idx >= 0 and score >= self.threshold:
            entry = self._entries[idx]
            return {
                "cached_from": entry["question"],
                "similarity": round(score, 3),
                "result": entry["result"],
            }
        return None

    def add(self, question: str, result: dict):
        self._index.add(self._embed(question))
        self._entries.append({"question": question, "result": result})
        
    def clear(self):
        self._index.reset()
        self._entries = []


cache = SemanticCache()