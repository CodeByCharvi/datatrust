from pathlib import Path

from fastapi import APIRouter, HTTPException, UploadFile
from pydantic import BaseModel, Field

from app.agents.pipeline import ask_datatrust
from app.services.rag import DOCS_DIR, store

router = APIRouter(prefix="/api")

MAX_UPLOAD_BYTES = 1_000_000


class AskRequest(BaseModel):
    question: str = Field(min_length=3, max_length=500)


@router.post("/ask")
def ask(request: AskRequest):
    return ask_datatrust(request.question)


@router.post("/upload")
async def upload(file: UploadFile):
    name = Path(file.filename or "").name
    if not name.lower().endswith((".txt", ".md")):
        raise HTTPException(status_code=400, detail="Only .txt and .md files are supported")

    raw = await file.read()
    if len(raw) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="File is larger than 1 MB")

    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File must be UTF-8 text")

    target = DOCS_DIR / name
    if target.exists():
        raise HTTPException(status_code=409, detail="A document with this name already exists")

    store.load_folder()  # make sure existing documents are indexed first
    target.write_text(text, encoding="utf-8")
    before = len(store.chunks)
    store.add_document(name, text)
    return {"filename": name, "chunks_added": len(store.chunks) - before}