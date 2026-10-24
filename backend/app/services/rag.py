import re
from pathlib import Path

import faiss
import numpy as np
from fastembed import TextEmbedding

from app.core.llm import ask_llm

DOCS_DIR = Path(__file__).resolve().parents[2] / "data"
MODEL_NAME = "BAAI/bge-small-en-v1.5"
DIMS = 384
TOP_K = 3

ANSWER_PROMPT = """You answer questions using ONLY the excerpts below.
If the answer is not in the excerpts, reply exactly: I could not find that in the document.
Do not use outside knowledge. Answer in 1-3 short sentences.

Excerpts:
{context}

Question: {question}"""


class DocumentStore:
    def __init__(self):
        self._model = None
        self._index = faiss.IndexFlatIP(DIMS)
        self.chunks = []
        self._loaded = False

    def _embed(self, texts):
        if self._model is None:
            self._model = TextEmbedding(MODEL_NAME)
        vecs = np.array(list(self._model.embed(texts)), dtype="float32")
        vecs /= np.linalg.norm(vecs, axis=1, keepdims=True)
        return vecs

    def add_document(self, name: str, text: str):
        parts = [p.strip() for p in re.split(r"\n\s*\n", text)]
        parts = [p for p in parts if len(p) >= 20]
        if not parts:
            return
        self._index.add(self._embed(parts))
        self.chunks.extend({"source": name, "text": p} for p in parts)

    def load_folder(self):
        if self._loaded:
            return
        for path in sorted(DOCS_DIR.glob("*.txt")) + sorted(DOCS_DIR.glob("*.md")):
                self.add_document(path.name, path.read_text(encoding="utf-8-sig"))
        self._loaded = True

    def search(self, question: str, k: int = TOP_K):
        if not self.chunks:
            return []
        scores, ids = self._index.search(self._embed([question]), min(k, len(self.chunks)))
        return [
            {**self.chunks[int(i)], "score": round(float(s), 3)}
            for s, i in zip(scores[0], ids[0])
            if int(i) >= 0
        ]


store = DocumentStore()


def ask_document(question: str) -> dict:
    store.load_folder()
    sources = store.search(question)
    if not sources:
        return {"answer": "No documents have been uploaded yet.", "sources": []}

    context = "\n\n".join(f"[{s['source']}]\n{s['text']}" for s in sources)
    answer = ask_llm(
        "You are a careful document assistant.",
        ANSWER_PROMPT.format(context=context, question=question),
    ).strip()
    return {"answer": answer, "sources": sources}
