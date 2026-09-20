# Vision RAG (Retrieval-Augmented Generation)

A multimodal retrieval-augmented generation system for vision and video datasets.

## Project Structure

```text
vision-rag/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── metadata/
│
├── models/
│
├── src/
│   ├── ingestion/
│   │   ├── image_loader.py
│   │   └── video_processor.py
│   ├── vision/
│   │   ├── detector.py
│   │   └── captioner.py
│   ├── embeddings/
│   │   └── embedder.py
│   ├── retrieval/
│   │   ├── faiss_store.py
│   │   └── search.py
│   ├── api/
│   │   └── main.py
│   └── utils/
│
├── notebooks/
├── tests/
├── requirements.txt
├── .gitignore
└── README.md
```

## Getting Started

### Installation
```bash
pip install -r requirements.txt
```

### Running the API
```bash
uvicorn src.api.main:app --reload
```
