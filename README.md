# VisionRAG

## Multimodal Image Semantic Search & Retrieval-Augmented Generation

VisionRAG is a multimodal AI application that enables users to search an image collection using natural-language queries.

The system combines **YOLO object detection, BLIP image captioning, spatial context generation, Sentence Transformers, FAISS vector search, query expansion, score fusion, and Gemini-powered Retrieval-Augmented Generation (RAG)** to retrieve visually relevant images and generate grounded answers.

The project provides a complete **React + FastAPI** application with dynamic image ingestion, automatic indexing, retrieval evaluation, and an interactive evaluation dashboard.

---

## Demo

### Core Workflow

```text
User Query
    |
    v
React Frontend
    |
    v
FastAPI Backend
    |
    v
Query Expansion
    |
    v
Sentence Transformer
    |
    v
FAISS Vector Search
    |
    v
Score Fusion + Filtering
    |
    v
Top-K Relevant Images
    |
    v
Gemini RAG
    |
    v
Grounded Answer
```

---

# Features

- Natural-language image search
- Semantic image retrieval
- YOLO-based object detection
- BLIP-based image captioning
- Spatial object understanding
- Multimodal visual context generation
- Sentence Transformer embeddings
- FAISS vector similarity search
- Query expansion using object synonyms
- Multi-query score fusion
- Similarity threshold filtering
- Object-based filtering
- Dynamic image upload
- Automatic image processing
- Automatic vector indexing
- Immediately searchable uploaded images
- Gemini-powered grounded RAG responses
- FastAPI REST API
- Swagger/OpenAPI documentation
- React frontend
- Tailwind CSS UI
- Retrieval evaluation
- Precision and recall metrics
- Evaluation dashboard
- API logging
- Input validation
- Docker support
- Docker Compose support

---

# Architecture

```text
                         +----------------------+
                         |        User          |
                         +----------+-----------+
                                    |
                                    v
                         +----------------------+
                         |    React Frontend    |
                         |     Vite + React     |
                         |     Tailwind CSS     |
                         +----------+-----------+
                                    |
                              HTTP / REST
                                    |
                                    v
                         +----------------------+
                         |    FastAPI Backend   |
                         +----------+-----------+
                                    |
                +-------------------+-------------------+
                |                   |                   |
                v                   v                   v
         Search Pipeline      Upload Pipeline      Evaluation
                |                   |                   |
                v                   v                   v
        Query Expansion        Save Image       results.json
                |
                v
       Sentence Transformer
                |
                v
          FAISS Search
                |
                v
      Score Fusion + Filtering
                |
                v
          Top-K Results
                |
                v
          Gemini RAG
                |
                v
        Grounded Answer
```

---

# Image Processing Pipeline

When an image is added to VisionRAG, it passes through the following pipeline:

```text
Image
  |
  v
YOLO Object Detection
  |
  +---- Object Classes
  |
  +---- Bounding Boxes
  |
  +---- Confidence Scores
  |
  v
BLIP Image Captioning
  |
  v
Spatial Position Analysis
  |
  v
Multimodal Visual Context
  |
  v
Sentence Transformer
  |
  v
384-Dimensional Embedding
  |
  v
FAISS Vector Index
```

The resulting metadata contains information such as:

- Image filename
- Image dimensions
- Detected objects
- Object confidence scores
- Bounding boxes
- Object positions
- Image caption
- Multimodal visual context

---

# Search Pipeline

A natural-language search query is processed as follows:

```text
User Query
    |
    v
Query Expansion
    |
    v
Multiple Query Variants
    |
    v
Sentence Transformer
    |
    v
FAISS Similarity Search
    |
    v
Candidate Results
    |
    v
Score Fusion
    |
    v
Similarity Filtering
    |
    v
Object Filtering
    |
    v
Top-K Results
    |
    v
Gemini RAG
    |
    v
Grounded Response
```

---

# Query Expansion

VisionRAG supports simple object-aware query expansion.

For example:

```text
car
```

can be expanded to:

```text
car
automobile
vehicle
```

Similarly:

```text
dog
```

can be expanded to:

```text
dog
puppy
canine
```

Word-boundary matching is used so that object names are not incorrectly replaced inside unrelated words.

For example, `carrot` will not be incorrectly transformed into variants such as `automobilerot`.

---

# Score Fusion

Each expanded query is independently searched against the FAISS index.

Candidate results are then combined.

The retrieval system uses:

```text
Average Similarity
        +
Consistency Bonus
        =
Final Retrieval Score
```

Results are sorted using the fused score before similarity filtering and top-K selection.

---

# Dynamic Image Indexing

VisionRAG supports adding new images without manually rebuilding the entire application.

The upload pipeline is:

```text
React Upload
     |
     v
FastAPI
     |
     v
Validate File
     |
     v
Save Image
     |
     v
YOLO Detection
     |
     v
BLIP Captioning
     |
     v
Multimodal Context
     |
     v
Sentence Transformer
     |
     v
FAISS Index
     |
     v
Reload Searcher
     |
     v
Immediately Searchable
```

Supported image formats:

```text
JPG
JPEG
PNG
WEBP
```

Maximum upload size:

```text
10 MB
```

---

# Retrieval-Augmented Generation

VisionRAG uses Gemini to generate grounded responses from retrieved visual evidence.

The RAG process is:

```text
User Query
     |
     v
FAISS Retrieval
     |
     v
Retrieved Images
     |
     +---- Caption
     |
     +---- Detected Objects
     |
     +---- Multimodal Context
     |
     v
Gemini
     |
     v
Grounded Answer
```

The generator is instructed to:

- Use only retrieved visual evidence
- Avoid inventing objects
- Avoid inventing people
- Avoid inventing locations
- Avoid unsupported claims
- State when evidence is insufficient
- Keep responses concise

### Important implementation detail

Gemini currently receives the **retrieved textual visual evidence** generated from the image pipeline rather than the raw image bytes.

The evidence includes:

- BLIP captions
- YOLO detected objects
- Object positions
- Multimodal visual context

---

# Technology Stack

## Programming Languages

- Python
- JavaScript

## Backend

- FastAPI
- Uvicorn
- Pydantic

## Computer Vision

- YOLO
- Ultralytics
- OpenCV
- BLIP
- PyTorch
- Torchvision

## Embeddings

- Sentence Transformers
- `all-MiniLM-L6-v2`

## Vector Search

- FAISS
- NumPy

## Generative AI

- Google Gemini API
- `google-genai`

## Frontend

- React
- Vite
- Tailwind CSS

## Infrastructure

- Docker
- Docker Compose

## Development Tools

- Git
- GitHub
- Swagger / OpenAPI

---

# Project Structure

```text
visonRag/
│
├── data/
│   ├── raw/
│   ├── processed/
│   ├── metadata/
│   │   ├── detections.json
│   │   └── multimodal_context.json
│   │
│   ├── evaluation/
│   │   ├── queries.json
│   │   └── results.json
│   │
│   └── faiss/
│       └── image_mapping.json
│
├── models/
│
├── src/
│   │
│   ├── api/
│   │   └── main.py
│   │
│   ├── embeddings/
│   │   └── embedder.py
│   │
│   ├── evaluation/
│   │   ├── generate_queries.py
│   │   └── evaluate_retrieval.py
│   │
│   ├── rag/
│   │   └── generator.py
│   │
│   ├── retrieval/
│   │   ├── faiss_store.py
│   │   ├── search.py
│   │   ├── query_expander.py
│   │   ├── build_index.py
│   │   └── index_single_image.py
│   │
│   └── vision/
│       ├── detector.py
│       ├── captioner.py
│       ├── spatial.py
│       ├── visualize.py
│       ├── multimodal_context.py
│       ├── process_single_image.py
│       └── generate_multimodal_context.py
│
├── frontend/
│   │
│   ├── src/
│   │   ├── components/
│   │   │   ├── SearchBar.jsx
│   │   │   ├── ResultCard.jsx
│   │   │   ├── ResultGrid.jsx
│   │   │   ├── ImageUpload.jsx
│   │   │   └── EvaluationDashboard.jsx
│   │   │
│   │   ├── App.jsx
│   │   ├── config.js
│   │   └── index.css
│   │
│   ├── package.json
│   └── vite.config.js
│
├── notebooks/
├── tests/
│
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

# API

VisionRAG exposes a REST API through FastAPI.

Swagger documentation is available at:

```text
http://127.0.0.1:8000/docs
```

---

## Health Check

### Endpoint

```http
GET /health
```

### Example Response

```json
{
  "status": "healthy",
  "service": "VisionRAG API",
  "indexed_images": 136
}
```

---

# Statistics

### Endpoint

```http
GET /stats
```

### Example Response

```json
{
  "indexed_images": 136,
  "embedding_dimension": 384
}
```

---

# Semantic Search

### Endpoint

```http
POST /search
```

### Request

```json
{
  "query": "images containing a dog",
  "top_k": 5,
  "min_score": 0.2,
  "object_filter": null
}
```

### Parameters

| Parameter | Type | Description |
|---|---|---|
| `query` | string | Natural-language search query |
| `top_k` | integer | Number of results to return |
| `min_score` | float | Minimum similarity score |
| `object_filter` | string/null | Optional detected-object filter |

### Response

The endpoint returns:

- Query
- Number of retrieved results
- Gemini-generated answer
- Retrieved image information
- Similarity scores
- Captions
- Detected objects
- Multimodal context

---

# Image Upload

### Endpoint

```http
POST /upload
```

### Supported formats

```text
.jpg
.jpeg
.png
.webp
```

### Maximum size

```text
10 MB
```

Uploaded images are automatically:

1. Saved to the raw image directory
2. Processed with YOLO
3. Captioned with BLIP
4. Converted into multimodal context
5. Embedded using Sentence Transformers
6. Added to the FAISS index
7. Made immediately searchable

---

# Image Retrieval

### Endpoint

```http
GET /images/{filename}
```

Returns the requested image from the image collection.

---

# Evaluation

### Endpoint

```http
GET /evaluation
```

Returns the complete retrieval evaluation results.

The endpoint powers the evaluation dashboard in the React frontend.

---

# Retrieval Evaluation

VisionRAG was evaluated using **30 object-oriented retrieval queries**.

Examples include:

```text
images containing a person
images containing a dog
images containing a car
images containing a pizza
images containing a book
```

The current evaluation results are:

| Metric | Result |
|---|---:|
| Evaluation Queries | 30 |
| Precision@1 | **90.00%** |
| Precision@3 | **84.44%** |
| Precision@5 | **68.00%** |
| Recall@5 | **81.77%** |
| Average Similarity | **0.513** |

---

# Evaluation Methodology

The evaluation dataset uses object-level relevance labels derived from YOLO detections.

For example:

```text
Image A
    |
    +---- detected: dog
```

means that Image A is considered relevant to:

```text
images containing a dog
```

The retrieval system then returns its top-K results, which are compared against these relevance labels.

Metrics calculated include:

- Precision@1
- Precision@3
- Precision@5
- Recall@5
- Average similarity

### Important limitation

The ground truth is derived from YOLO detections.

Therefore, the reported metrics measure retrieval performance against **YOLO-derived object-level relevance labels** rather than human relevance judgments.

---

# Evaluation Dashboard

The frontend provides an evaluation dashboard containing:

```text
+----------------+----------------+
| Precision@1    | Precision@3    |
| 90.0%          | 84.4%          |
+----------------+----------------+

+----------------+----------------+
| Precision@5    | Recall@5       |
| 68.0%          | 81.8%          |
+----------------+----------------+

+-------------------------------+
| Average Similarity            |
| 0.513                         |
+-------------------------------+
```

The dashboard also provides query-level metrics for each evaluation query.

---

# Logging

VisionRAG includes structured application logging.

Example:

```text
2026-09-23 18:00:01 | INFO | visionrag |
Search request received | query='images containing a dog'

2026-09-23 18:00:02 | INFO | visionrag |
Semantic retrieval completed | results=5

2026-09-23 18:00:02 | INFO | visionrag |
Starting Gemini RAG generation

2026-09-23 18:00:04 | INFO | visionrag |
Gemini RAG generation completed
```

Logging is used for:

- API requests
- Search operations
- Image uploads
- Image processing
- Dynamic indexing
- Search index reloads
- Evaluation requests
- Errors and exceptions

---

# Error Handling

The backend validates:

- Empty search queries
- Invalid `top_k`
- Invalid similarity thresholds
- Missing upload filenames
- Unsupported image formats
- Empty uploads
- Oversized uploads
- Missing images
- Missing evaluation results

The upload API limits images to:

```text
10 MB
```

---

# Running Locally

## 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd visonRag
```

---

## 2. Create a virtual environment

```bash
python -m venv venv
```

### Windows PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

---

## 3. Install Python dependencies

```powershell
pip install -r requirements.txt
```

---

# 4. Configure Gemini

Create a `.env` file in the project root:

```text
GEMINI_API_KEY=your_actual_gemini_api_key
```

Never commit `.env` to Git.

A template is provided as:

```text
.env.example
```

---

# 5. Start the FastAPI backend

From the project root:

```powershell
uvicorn src.api.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

---

# 6. Start the React frontend

Open another terminal:

```powershell
cd frontend
npm install
npm run dev
```

Frontend:

```text
http://localhost:5173
```

---

# Frontend Environment Configuration

The frontend uses:

```javascript
export const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  "http://127.0.0.1:8000";
```

For local development:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

For production:

```env
VITE_API_BASE_URL=https://your-api-domain.com
```

---

# Docker

VisionRAG includes Docker support for the FastAPI backend.

## Build

```bash
docker compose build
```

## Run

```bash
docker compose up
```

The backend will be available at:

```text
http://localhost:8000
```

> Docker support is included in the project. Full Docker build/deployment verification should be performed in the target environment before claiming a production deployment.

---

# Docker Architecture

```text
+----------------------------+
|      Docker Container      |
|                            |
|       FastAPI Backend      |
|             |              |
|     +-------+-------+      |
|     |       |       |      |
|    YOLO   BLIP   Gemini     |
|     |       |       |      |
|     +-------+-------+      |
|             |              |
|          FAISS             |
|                            |
+----------------------------+
             |
             |
       Mounted ./data
```

---

# Security

Secrets are stored using environment variables.

The Gemini API key should be provided through:

```text
.env
```

and must never be committed to the repository.

The `.gitignore` file excludes:

```text
.env
venv/
node_modules/
dist/
logs/
```

---

# Key Engineering Concepts

This project demonstrates practical implementation of:

### Machine Learning

- Computer vision pipelines
- Object detection
- Image captioning
- Embeddings

### Information Retrieval

- Dense vector retrieval
- FAISS similarity search
- Query expansion
- Score fusion
- Similarity filtering
- Object filtering
- Retrieval evaluation

### Generative AI

- Retrieval-Augmented Generation
- Grounded generation
- Context construction
- Gemini API integration

### Backend Development

- REST APIs
- FastAPI
- Pydantic validation
- File uploads
- Error handling
- Logging
- OpenAPI / Swagger

### Frontend Development

- React
- Vite
- Tailwind CSS
- REST API integration
- Search interface
- Upload interface
- Evaluation dashboard

### Deployment

- Docker
- Docker Compose
- Environment configuration

---

# Development Phases

The project was developed incrementally.

```text
Phase 1   Image ingestion
Phase 2   YOLO object detection
Phase 3   Visual context generation
Phase 4   Embeddings + FAISS
Phase 5   Multimodal visual understanding
Phase 6   Semantic search + evaluation
Phase 7   FastAPI backend
Phase 8   React frontend
Phase 9   Gemini RAG
Phase 10  Query expansion + score fusion
Phase 11  Dynamic image indexing
Phase 12  Retrieval evaluation dashboard
Phase 13  Production polish
```

---

# Future Improvements

Potential improvements include:

- CLIP-based image-text embeddings
- Hybrid lexical + vector retrieval
- Cross-encoder re-ranking
- Recall@10 and Recall@20
- mAP evaluation
- NDCG evaluation
- Human relevance evaluation
- Authentication and authorization
- GPU inference
- Cloud deployment
- Distributed vector databases
- Image-aware multimodal LLM input
- Background task processing for uploads
- Async inference pipelines
- Model caching
- Monitoring and observability

---

# Why VisionRAG?

VisionRAG demonstrates how multiple AI components can be combined into a complete production-oriented application:

```text
Computer Vision
       +
Semantic Embeddings
       +
Vector Retrieval
       +
Query Processing
       +
RAG
       +
FastAPI
       +
React
       +
Docker
```

Instead of treating computer vision, retrieval, and generative AI as isolated components, VisionRAG connects them into a single end-to-end system.

---

# Project Highlights

- Multimodal visual understanding
- Semantic image retrieval
- Dynamic vector indexing
- Query expansion and score fusion
- Retrieval evaluation
- Gemini-powered RAG
- Full-stack implementation
- REST API
- Interactive frontend
- Docker support
- Production-oriented logging and validation

---

# Author

**Krishna Guru Sai**

Computer Science Engineering Student

Interested in:

- Machine Learning
- Computer Vision
- Generative AI
- Retrieval-Augmented Generation
- Backend Engineering
- Full-Stack AI Applications
