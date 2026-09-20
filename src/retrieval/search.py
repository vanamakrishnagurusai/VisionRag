from pathlib import Path
import json

from src.embeddings.embedder import TextEmbedder
from src.retrieval.faiss_store import FAISSStore


PROJECT_ROOT = Path(__file__).resolve().parents[2]

FAISS_DIR = (
    PROJECT_ROOT
    / "data"
    / "faiss"
)

INDEX_FILE = (
    FAISS_DIR
    / "image_index.faiss"
)

MAPPING_FILE = (
    FAISS_DIR
    / "image_mapping.json"
)


class ImageSearcher:

    def __init__(self):

        self.embedder = TextEmbedder()

        self.store = FAISSStore.load(
            INDEX_FILE
        )

        with open(
            MAPPING_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            self.mapping = json.load(f)

    def search(
        self,
        query,
        top_k=5
    ):

        query_embedding = (
            self.embedder.encode(
                [query]
            )
        )

        scores, indices = (
            self.store.search(
                query_embedding,
                top_k
            )
        )

        results = []

        for score, index in zip(
            scores[0],
            indices[0]
        ):

            if index < 0:
                continue

            item = self.mapping[index]

            results.append(
                {
                    "score": float(score),
                    "filename": item["filename"],
                    "filepath": item["filepath"],
                    "visual_context": item[
                        "visual_context"
                    ]
                }
            )

        return results


def main():

    searcher = ImageSearcher()

    print(
        "\nVisionRAG Semantic Search"
    )

    print(
        "Type 'exit' to quit.\n"
    )

    while True:

        query = input(
            "Search: "
        )

        if query.lower() == "exit":
            break

        results = searcher.search(
            query,
            top_k=5
        )

        print(
            "\nResults:"
        )

        for i, result in enumerate(
            results,
            start=1
        ):

            print(
                f"\n{i}. "
                f"{result['filename']}"
            )

            print(
                f"Score: "
                f"{result['score']:.4f}"
            )

            print(
                f"Context: "
                f"{result['visual_context']}"
            )

        print()


if __name__ == "__main__":
    main()