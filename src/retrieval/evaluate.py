from pathlib import Path
import json

from src.retrieval.search import ImageSearcher


PROJECT_ROOT = Path(__file__).resolve().parents[2]

EVALUATION_FILE = (
    PROJECT_ROOT
    / "data"
    / "evaluation"
    / "queries.json"
)


def precision_at_k(
    retrieved,
    relevant,
    k
):

    retrieved = retrieved[:k]

    if not retrieved:
        return 0.0

    relevant_count = sum(
        1
        for item in retrieved
        if item in relevant
    )

    return relevant_count / len(
        retrieved
    )


def main():

    with open(
        EVALUATION_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        queries = json.load(f)

    searcher = ImageSearcher()

    k = 5

    scores = []

    for item in queries:

        query = item["query"]

        relevant = set(
            item["relevant_images"]
        )

        results = searcher.search(
            query,
            top_k=k
        )

        retrieved = [
            result["filename"]
            for result in results
        ]

        score = precision_at_k(
            retrieved,
            relevant,
            k
        )

        scores.append(score)

        print(
            f"\nQuery: {query}"
        )

        print(
            f"Retrieved: {retrieved}"
        )

        print(
            f"Precision@{k}: "
            f"{score:.3f}"
        )

    if scores:

        mean_score = (
            sum(scores)
            / len(scores)
        )

        print(
            "\n=============================="
        )

        print(
            f"Mean Precision@{k}: "
            f"{mean_score:.3f}"
        )


if __name__ == "__main__":
    main()