from pathlib import Path
import json

from src.embeddings.embedder import TextEmbedder
from src.retrieval.faiss_store import FAISSStore


PROJECT_ROOT = Path(__file__).resolve().parents[2]

METADATA_DIR = (
    PROJECT_ROOT
    / "data"
    / "metadata"
)

INDEX_DIR = (
    PROJECT_ROOT
    / "data"
    / "faiss"
)

INPUT_FILE = (
    METADATA_DIR
    / "visual_context.json"
)

INDEX_FILE = (
    INDEX_DIR
    / "image_index.faiss"
)

MAPPING_FILE = (
    INDEX_DIR
    / "image_mapping.json"
)


def build_index():

    INDEX_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # ----------------------------------------
    # Load metadata
    # ----------------------------------------

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        image_data = json.load(f)

    print(
        f"Loaded {len(image_data)} images."
    )

    # ----------------------------------------
    # Extract contexts
    # ----------------------------------------

    contexts = [
        item["visual_context"]
        for item in image_data
    ]

    # ----------------------------------------
    # Generate embeddings
    # ----------------------------------------

    embedder = TextEmbedder()

    embeddings = embedder.encode(
        contexts
    )

    print(
        "Embedding shape:",
        embeddings.shape
    )

    # ----------------------------------------
    # Build FAISS index
    # ----------------------------------------

    dimension = embeddings.shape[1]

    store = FAISSStore(
        dimension
    )

    store.add(
        embeddings
    )

    # ----------------------------------------
    # Save FAISS index
    # ----------------------------------------

    store.save(
        INDEX_FILE
    )

    # ----------------------------------------
    # Save mapping
    # ----------------------------------------

    mapping = []

    for index, item in enumerate(image_data):

        mapping.append(
            {
                "faiss_index": index,
                "image_id": item["image_id"],
                "filename": item["filename"],
                "filepath": item["filepath"],
                "visual_context": item["visual_context"]
            }
        )

    with open(
        MAPPING_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            mapping,
            f,
            indent=4
        )

    print(
        "\nFAISS index saved to:"
    )

    print(INDEX_FILE)

    print(
        "\nMapping saved to:"
    )

    print(MAPPING_FILE)


if __name__ == "__main__":
    build_index()