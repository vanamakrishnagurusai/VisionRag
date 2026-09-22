import json
from pathlib import Path

from src.embeddings.embedder import TextEmbedder
from src.retrieval.faiss_store import FAISSStore


PROJECT_ROOT = Path(__file__).resolve().parents[2]

FAISS_DIR = (
    PROJECT_ROOT
    / "data"
    / "faiss"
)

INDEX_PATH = (
    FAISS_DIR
    / "image_index.faiss"
)

MAPPING_PATH = (
    FAISS_DIR
    / "image_mapping.json"
)

MULTIMODAL_CONTEXT_PATH = (
    PROJECT_ROOT
    / "data"
    / "metadata"
    / "multimodal_context.json"
)


def index_single_image():

    # ----------------------------------------------
    # Load multimodal metadata
    # ----------------------------------------------

    with open(
        MULTIMODAL_CONTEXT_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        metadata = json.load(file)

    if not metadata:
        raise ValueError(
            "No multimodal metadata found."
        )

    # ----------------------------------------------
    # Load FAISS
    # ----------------------------------------------

    store = FAISSStore.load(
        INDEX_PATH
    )

    # ----------------------------------------------
    # Load embedding model
    # ----------------------------------------------

    embedder = TextEmbedder()

    # ----------------------------------------------
    # Load existing mapping
    # ----------------------------------------------

    with open(
        MAPPING_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        mapping = json.load(file)

    existing_files = {
        item["filename"]
        for item in mapping
    }

    # ----------------------------------------------
    # Find images not already indexed
    # ----------------------------------------------

    new_items = [
        item
        for item in metadata
        if item["filename"]
        not in existing_files
    ]

    if not new_items:

        print(
            "No new images to index."
        )

        return

    # ----------------------------------------------
    # Generate embeddings
    # ----------------------------------------------

    texts = [
        item["multimodal_context"]
        for item in new_items
    ]

    embeddings = embedder.encode(
        texts
    )

    # ----------------------------------------------
    # Add embeddings to FAISS
    # ----------------------------------------------

    store.add(
        embeddings
    )

    # ----------------------------------------------
    # Add mapping entries
    # ----------------------------------------------

    start_index = store.index.ntotal

    for offset, item in enumerate(
        new_items
    ):

        mapping.append(
            {
                "faiss_index": (
                    start_index + offset
                ),
                "image_id": item.get(
                    "image_id",
                    ""
                ),
                "filename": item.get(
                    "filename",
                    ""
                ),
                "filepath": item.get(
                    "filepath",
                    ""
                ),
                "caption": item.get(
                    "caption",
                    ""
                ),
                "multimodal_context": item.get(
                    "multimodal_context",
                    ""
                ),
                "objects": item.get(
                    "objects",
                    []
                )
            }
        )

    # ----------------------------------------------
    # Save FAISS
    # ----------------------------------------------

    store.save(
        INDEX_PATH
    )

    # ----------------------------------------------
    # Save mapping
    # ----------------------------------------------

    with open(
        MAPPING_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            mapping,
            file,
            indent=2
        )

    print(
        f"Indexed {len(new_items)} new image(s)."
    )


if __name__ == "__main__":
    index_single_image()