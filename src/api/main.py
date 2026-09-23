import json
import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from src.retrieval.search import ImageSearcher
from src.rag.generator import RAGGenerator
from src.vision.process_single_image import process_single_image
from src.retrieval.index_single_image import index_single_image


# --------------------------------------------------
# Logging configuration
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logger = logging.getLogger("visionrag")


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

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


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

logger.info("Loading VisionRAG search system...")

searcher = ImageSearcher()

logger.info(
    "VisionRAG search system loaded | vectors=%s",
    searcher.store.index.ntotal
)

logger.info("Loading Gemini RAG generator...")

rag_generator = RAGGenerator()

logger.info("Gemini RAG generator loaded successfully.")


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

    logger.info("Health check requested")

    return {
        "status": "healthy",
        "service": "VisionRAG API",
        "indexed_images": searcher.store.index.ntotal
    }


# --------------------------------------------------
# Statistics
# --------------------------------------------------

@app.get("/stats")
def get_stats():

    logger.info("Statistics requested")

    return {
        "indexed_images": searcher.store.index.ntotal,
        "embedding_dimension": searcher.store.dimension,
    }


# --------------------------------------------------
# Semantic Search + RAG
# --------------------------------------------------

@app.post("/search", response_model=SearchResponse)
def search_images(request: SearchRequest):

    logger.info(
        "Search request received | query='%s' | top_k=%s | min_score=%s | object_filter='%s'",
        request.query,
        request.top_k,
        request.min_score,
        request.object_filter
    )

    # ----------------------------------------------
    # Validate query
    # ----------------------------------------------

    if not request.query.strip():

        logger.warning("Search rejected because query is empty.")

        raise HTTPException(
            status_code=400,
            detail="Search query cannot be empty."
        )

    # ----------------------------------------------
    # Validate top_k
    # ----------------------------------------------

    if request.top_k < 1 or request.top_k > 20:

        logger.warning(
            "Search rejected because top_k=%s is invalid.",
            request.top_k
        )

        raise HTTPException(
            status_code=400,
            detail="top_k must be between 1 and 20."
        )

    # ----------------------------------------------
    # Validate min_score
    # ----------------------------------------------

    if request.min_score < -1.0 or request.min_score > 1.0:

        logger.warning(
            "Search rejected because min_score=%s is invalid.",
            request.min_score
        )

        raise HTTPException(
            status_code=400,
            detail="min_score must be between -1.0 and 1.0."
        )

    try:

        # ------------------------------------------
        # Step 1: Retrieve relevant images using FAISS
        # ------------------------------------------

        logger.info(
            "Starting semantic retrieval | query='%s'",
            request.query
        )

        results = searcher.search(
            query=request.query,
            top_k=request.top_k,
            min_score=request.min_score,
            object_filter=request.object_filter
        )

        logger.info(
            "Semantic retrieval completed | query='%s' | results=%s",
            request.query,
            len(results)
        )

        # ------------------------------------------
        # Step 2: Generate grounded answer using Gemini
        # ------------------------------------------

        logger.info(
            "Starting Gemini RAG generation | query='%s'",
            request.query
        )

        answer = rag_generator.generate_answer(
            request.query,
            results
        )

        logger.info(
            "Gemini RAG generation completed | query='%s'",
            request.query
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

    except Exception:

        logger.exception(
            "Search failed | query='%s'",
            request.query
        )

        raise HTTPException(
            status_code=500,
            detail="Search failed."
        )


# --------------------------------------------------
# Upload image
# --------------------------------------------------

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):

    global searcher

    logger.info(
        "Image upload request received | filename='%s'",
        file.filename
    )

    allowed_extensions = {
        ".jpg",
        ".jpeg",
        ".png",
        ".webp"
    }

    # ----------------------------------------------
    # Validate filename
    # ----------------------------------------------

    if not file.filename:

        logger.warning(
            "Upload rejected because filename was missing."
        )

        raise HTTPException(
            status_code=400,
            detail="No filename provided."
        )

    # ----------------------------------------------
    # Sanitize filename
    # ----------------------------------------------

    original_name = Path(file.filename).name

    extension = Path(original_name).suffix.lower()

    # ----------------------------------------------
    # Validate file extension
    # ----------------------------------------------

    if extension not in allowed_extensions:

        logger.warning(
            "Upload rejected | unsupported extension='%s'",
            extension
        )

        raise HTTPException(
            status_code=400,
            detail="Unsupported image format. Use JPG, JPEG, PNG or WEBP."
        )

    RAW_IMAGE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    image_path = RAW_IMAGE_DIR / original_name

    # ----------------------------------------------
    # Save uploaded image
    # ----------------------------------------------

    try:

        contents = await file.read()

        # Empty file validation
        if not contents:

            logger.warning(
                "Upload rejected because file is empty | filename='%s'",
                original_name
            )

            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty."
            )

        # File size validation
        if len(contents) > MAX_FILE_SIZE:

            logger.warning(
                "Upload rejected because file exceeds 10 MB | filename='%s' | size=%s bytes",
                original_name,
                len(contents)
            )

            raise HTTPException(
                status_code=413,
                detail="Image size must be less than 10 MB."
            )

        # Save file
        with open(
            image_path,
            "wb"
        ) as output_file:

            output_file.write(contents)

        logger.info(
            "Image saved successfully | filename='%s' | size=%s bytes",
            original_name,
            len(contents)
        )

    except HTTPException:
        raise

    except Exception:

        logger.exception(
            "Failed to save uploaded image | filename='%s'",
            original_name
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to save image."
        )

    # ----------------------------------------------
    # Process and dynamically index image
    # ----------------------------------------------

    try:

        # ------------------------------------------
        # Process image
        # ------------------------------------------

        logger.info(
            "Starting image processing | filename='%s'",
            original_name
        )

        result = process_single_image(
            image_path
        )

        logger.info(
            "Image processing completed | filename='%s'",
            original_name
        )

        # ------------------------------------------
        # Dynamic indexing
        # ------------------------------------------

        logger.info(
            "Starting dynamic indexing | filename='%s'",
            original_name
        )

        index_single_image()

        logger.info(
            "Dynamic indexing completed | filename='%s'",
            original_name
        )

        # ------------------------------------------
        # Reload searcher
        # ------------------------------------------

        logger.info(
            "Reloading search index..."
        )

        searcher = ImageSearcher()

        logger.info(
            "Search index reloaded | vectors=%s",
            searcher.store.index.ntotal
        )

    except Exception:

        logger.exception(
            "Image processing or indexing failed | filename='%s'",
            original_name
        )

        # Remove uploaded image if processing failed
        if image_path.exists():

            try:
                image_path.unlink()

                logger.info(
                    "Removed failed upload | filename='%s'",
                    original_name
                )

            except Exception:

                logger.exception(
                    "Failed to remove uploaded image after processing failure | filename='%s'",
                    original_name
                )

        raise HTTPException(
            status_code=500,
            detail="Image processing or indexing failed."
        )

    # ----------------------------------------------
    # Successful upload response
    # ----------------------------------------------

    logger.info(
        "Image upload completed successfully | filename='%s'",
        original_name
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

    logger.info(
        "Image requested | filename='%s'",
        filename
    )

    # Sanitize filename
    safe_filename = Path(filename).name

    image_path = RAW_IMAGE_DIR / safe_filename

    if not image_path.exists():

        logger.warning(
            "Image not found | filename='%s'",
            safe_filename
        )

        raise HTTPException(
            status_code=404,
            detail="Image not found."
        )

    return FileResponse(
        image_path
    )


# --------------------------------------------------
# Evaluation results
# --------------------------------------------------

@app.get("/evaluation")
def get_evaluation():

    logger.info(
        "Evaluation results requested"
    )

    if not EVALUATION_RESULTS_PATH.exists():

        logger.warning(
            "Evaluation results file not found | path='%s'",
            EVALUATION_RESULTS_PATH
        )

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

            data = json.load(file)

        logger.info(
            "Evaluation results loaded | queries=%s",
            data.get("overall", {}).get("queries", 0)
        )

        return data

    except Exception:

        logger.exception(
            "Failed to load evaluation results"
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to load evaluation results."
        )