from pathlib import Path
import json
from fastapi import (
    FastAPI,
    HTTPException,
    UploadFile,
    File
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from src.retrieval.search import ImageSearcher
from src.rag.generator import RAGGenerator
from src.vision.process_single_image import process_single_image
from src.retrieval.index_single_image import index_single_image
# --------------------------------------------------
# Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_IMAGE_DIR = PROJECT_ROOT / "data" / "raw"
EVALUATION_RESULTS_PATH = (
    PROJECT_ROOT
    / "data"
    / "evaluation"
    / "results.json"
)

# --------------------------------------------------
# FastAPI application
# --------------------------------------------------

app = FastAPI(
    title="VisionRAG API",
    description="Multimodal image semantic search and RAG API",
    version="1.0.0"
)


# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Initialize services
# --------------------------------------------------

searcher = ImageSearcher()
rag_generator = RAGGenerator()


# --------------------------------------------------
# Request / Response models
# --------------------------------------------------

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5
    min_score: float = 0.20
    object_filter: str | None = None


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
    answer: str
    results: list[SearchResult]


# --------------------------------------------------
# Health check
# --------------------------------------------------

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "VisionRAG API"
    }


# --------------------------------------------------
# Statistics
# --------------------------------------------------

@app.get("/stats")
def get_stats():

    return {
        "indexed_images": searcher.store.index.ntotal,
        "embedding_dimension": searcher.store.dimension,
    }


# --------------------------------------------------
# Semantic Search + RAG
# --------------------------------------------------

@app.post("/search", response_model=SearchResponse)
def search_images(request: SearchRequest):

    # Validate query
    if not request.query.strip():
        raise HTTPException(
            status_code=400,
            detail="Search query cannot be empty."
        )

    # Validate top_k
    if request.top_k < 1 or request.top_k > 20:
        raise HTTPException(
            status_code=400,
            detail="top_k must be between 1 and 20."
        )

    try:

        # ------------------------------------------
        # Step 1: Retrieve relevant images using FAISS
        # ------------------------------------------

        results = searcher.search(
        query=request.query,
        top_k=request.top_k,
        min_score=request.min_score,
        object_filter=request.object_filter
        )

        # ------------------------------------------
        # Step 2: Generate grounded answer using Gemini
        # ------------------------------------------

        answer = rag_generator.generate_answer(
            request.query,
            results
        )

        # ------------------------------------------
        # Step 3: Return results + generated answer
        # ------------------------------------------

        return SearchResponse(
            query=request.query,
            count=len(results),
            answer=answer,
            results=results
        )

    except Exception as e:

        print(f"Search error: {e}")

        raise HTTPException(
            status_code=500,
            detail=f"Search failed: {str(e)}"
        )



# --------------------------------------------------
# Upload image
# --------------------------------------------------

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    global searcher
    allowed_extensions = {".jpg", ".jpeg", ".png", ".webp"}

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No filename provided."
        )

    original_name = Path(file.filename).name
    extension = Path(original_name).suffix.lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Unsupported image format. Use JPG, JPEG, PNG or WEBP."
        )

    RAW_IMAGE_DIR.mkdir(parents=True, exist_ok=True)

    image_path = RAW_IMAGE_DIR / original_name

    try:
        contents = await file.read()

        with open(image_path, "wb") as output_file:
            output_file.write(contents)

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save image: {error}"
        )

    try:
        result = process_single_image(image_path)

        print("=== STARTING DYNAMIC INDEXING ===")

        index_single_image()

        print("=== DYNAMIC INDEXING FINISHED ===")

        searcher = ImageSearcher()

        print(
            f"Reloaded searcher with {searcher.store.index.ntotal} vectors."
        )

    except Exception as error:

        if image_path.exists():
            image_path.unlink()

        raise HTTPException(
            status_code=500,
            detail=f"Image processing or indexing failed: {error}"
        )

    return {
        "message": "Image uploaded, processed and indexed successfully.",
        "image": result
    }

# --------------------------------------------------
# Serve images
# --------------------------------------------------

@app.get("/images/{filename}")
def get_image(filename: str):

    image_path = RAW_IMAGE_DIR / filename

    if not image_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Image not found."
        )

    return FileResponse(
        image_path
    )

@app.get("/evaluation")
def get_evaluation():
    if not EVALUATION_RESULTS_PATH.exists():
        raise HTTPException(
            status_code=404,
            detail="Evaluation results not found."
        )

    try:
        with open(
            EVALUATION_RESULTS_PATH,
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to load evaluation results: {error}"
        )