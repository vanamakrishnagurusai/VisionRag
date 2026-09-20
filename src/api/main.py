from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
from src.retrieval.search import ImageSearcher
from fastapi.middleware.cors import CORSMiddleware

# ============================================================
# Project paths
# ============================================================


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DIR = (
    PROJECT_ROOT
    / "data"
    / "raw"
)


# ============================================================
# FastAPI application
# ============================================================

app = FastAPI(
    title="VisionRAG API",
    description=(
        "Multimodal image semantic search "
        "using YOLO, BLIP, embeddings and FAISS."
    ),
    version="1.0.0"
)


# ============================================================
# Load search engine
# ============================================================

searcher = ImageSearcher()


# ============================================================
# Request schema
# ============================================================
class SearchResult(BaseModel):

    rank: int

    score: float

    filename: str

    filepath: str

    image_url: str

    caption: str

    multimodal_context: str

    objects: list

class SearchResponse(BaseModel):

    query: str

    count: int

    results: List[SearchResult]
    
class SearchRequest(BaseModel):

    query: str

    top_k: int = 5


# ============================================================
# Health endpoint
# ============================================================

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "service": "VisionRAG API"
    }


# ============================================================
# Search endpoint
# ============================================================

@app.post(
    "/search",
    response_model=SearchResponse
)
def search_images(
    request: SearchRequest
):

    query = request.query.strip()

    if not query:

        raise HTTPException(
            status_code=400,
            detail="Query cannot be empty."
        )

    if request.top_k <= 0:

        raise HTTPException(
            status_code=400,
            detail="top_k must be greater than 0."
        )

    results = searcher.search(
        query,
        top_k=request.top_k
    )

    return {
        "query": query,
        "count": len(results),
        "results": results
    }


# ============================================================
# Image endpoint
# ============================================================

@app.get("/images/{filename}")
def get_image(
    filename: str
):

    image_path = RAW_DIR / filename

    if not image_path.exists():

        raise HTTPException(
            status_code=404,
            detail="Image not found."
        )

    return FileResponse(
        image_path
    )
@app.get("/stats")
def get_stats():

    return {
        "indexed_images": len(
            searcher.mapping
        ),
        "embedding_dimension": (
            searcher.store.dimension
        ),
        "faiss_vectors": (
            searcher.store.index.ntotal
        )
    }



app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)