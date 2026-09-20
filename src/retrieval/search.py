from pathlib import Path
import json

from src.embeddings.embedder import TextEmbedder
from src.retrieval.faiss_store import FAISSStore


PROJECT_ROOT = Path(__file__).resolve().parents[2]

FAISS_DIR = PROJECT_ROOT / "data" / "faiss"

INDEX_FILE = FAISS_DIR / "image_index.faiss"

MAPPING_FILE = FAISS_DIR / "image_mapping.json"


class ImageSearcher:

    def __init__(self):

        print("Loading search system...")

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

        print(
            f"Loaded {len(self.mapping)} images."
        )

    def search(
    self,
    query,
    top_k=5,
    min_score=0.20
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
            
            if score < min_score:
                continue
            
            item = self.mapping[index]

            results.append(
                {
                    "rank": len(results) + 1,
                    "score": float(score),
                    "filename": item[
                        "filename"
                    ],
                    "filepath": item[
                        "filepath"
                    ],
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

        return results


def print_results(
    query,
    results
):

    print("\n" + "=" * 70)

    print(
        f"QUERY: {query}"
    )

    print("=" * 70)

    if not results:

        print("No results found.")

        return

    for result in results:

        print(
            f"\n#{result['rank']} "
            f"{result['filename']}"
        )

        print(
            f"Similarity: "
            f"{result['score']:.4f}"
        )

        print(
            f"Caption: "
            f"{result['caption']}"
        )

        print(
            f"Context: "
            f"{result['multimodal_context']}"
        )

        objects = [
            obj["class"]
            for obj in result["objects"]
        ]

        print(
            f"Objects: "
            f"{', '.join(objects) if objects else 'None'}"
        )

        print(
            f"Path: "
            f"{result['filepath']}"
        )


def main():

    searcher = ImageSearcher()

    print(
        "\nVisionRAG Semantic Search"
    )

    print(
        "Type 'exit' to quit."
    )

    while True:

        query = input(
            "\nSearch: "
        ).strip()

        if query.lower() == "exit":
            break

        if not query:
            continue

        results = searcher.search(
            query,
            top_k=5
        )

        print_results(
            query,
            results
        )


if __name__ == "__main__":
    main()