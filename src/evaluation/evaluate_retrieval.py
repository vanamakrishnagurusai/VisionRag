import json
from pathlib import Path

from src.retrieval.search import ImageSearcher


PROJECT_ROOT = Path(__file__).resolve().parents[2]

QUERIES_PATH = (
    PROJECT_ROOT
    / "data"
    / "evaluation"
    / "queries.json"
)

RESULTS_PATH = (
    PROJECT_ROOT
    / "data"
    / "evaluation"
    / "results.json"
)


def precision_at_k(retrieved, relevant, k):
    """
    Precision@K =
    relevant retrieved images / K
    """

    retrieved_at_k = retrieved[:k]

    if not retrieved_at_k:
        return 0.0

    relevant_count = sum(
        1
        for filename in retrieved_at_k
        if filename in relevant
    )

    return relevant_count / len(retrieved_at_k)


def recall_at_k(retrieved, relevant, k):
    """
    Recall@K =
    relevant retrieved images / total relevant images
    """

    if not relevant:
        return 0.0

    retrieved_at_k = retrieved[:k]

    relevant_count = sum(
        1
        for filename in retrieved_at_k
        if filename in relevant
    )

    return relevant_count / len(relevant)


def evaluate_query(searcher, query_data):

    query = query_data["query"]

    relevant_images = set(
        query_data["relevant_images"]
    )

    results = searcher.search(
        query=query,
        top_k=5,
        min_score=0.0
    )

    retrieved_images = [
        result["filename"]
        for result in results
    ]

    similarities = [
        result["score"]
        for result in results
    ]

    return {
        "query": query,
        "relevant_count": len(relevant_images),
        "retrieved": retrieved_images,

        "precision_at_1": precision_at_k(
            retrieved_images,
            relevant_images,
            1
        ),

        "precision_at_3": precision_at_k(
            retrieved_images,
            relevant_images,
            3
        ),

        "precision_at_5": precision_at_k(
            retrieved_images,
            relevant_images,
            5
        ),

        "recall_at_5": recall_at_k(
            retrieved_images,
            relevant_images,
            5
        ),

        "average_similarity": (
            sum(similarities) / len(similarities)
            if similarities
            else 0.0
        )
    }


def main():

    print("Loading evaluation queries...")

    with open(
        QUERIES_PATH,
        "r",
        encoding="utf-8"
    ) as file:
        queries = json.load(file)

    print(
        f"Loaded {len(queries)} evaluation queries."
    )

    print("\nLoading VisionRAG search system...")

    searcher = ImageSearcher()

    evaluation_results = []

    for index, query_data in enumerate(
        queries,
        start=1
    ):

        print(
            f"\n[{index}/{len(queries)}] "
            f"{query_data['query']}"
        )

        result = evaluate_query(
            searcher,
            query_data
        )

        evaluation_results.append(result)

        print(
            f"Precision@1: "
            f"{result['precision_at_1']:.3f}"
        )

        print(
            f"Precision@3: "
            f"{result['precision_at_3']:.3f}"
        )

        print(
            f"Precision@5: "
            f"{result['precision_at_5']:.3f}"
        )

        print(
            f"Recall@5: "
            f"{result['recall_at_5']:.3f}"
        )

        print(
            f"Average similarity: "
            f"{result['average_similarity']:.3f}"
        )

    # ------------------------------------------------
    # Calculate overall metrics
    # ------------------------------------------------

    query_count = len(evaluation_results)

    if query_count == 0:
        raise ValueError(
            "No evaluation results generated."
        )

    overall = {
        "queries": query_count,

        "precision_at_1": (
            sum(
                r["precision_at_1"]
                for r in evaluation_results
            )
            / query_count
        ),

        "precision_at_3": (
            sum(
                r["precision_at_3"]
                for r in evaluation_results
            )
            / query_count
        ),

        "precision_at_5": (
            sum(
                r["precision_at_5"]
                for r in evaluation_results
            )
            / query_count
        ),

        "recall_at_5": (
            sum(
                r["recall_at_5"]
                for r in evaluation_results
            )
            / query_count
        ),

        "average_similarity": (
            sum(
                r["average_similarity"]
                for r in evaluation_results
            )
            / query_count
        )
    }

    output = {
        "overall": overall,
        "queries": evaluation_results
    }

    RESULTS_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        RESULTS_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            output,
            file,
            indent=2
        )

    # ------------------------------------------------
    # Print summary
    # ------------------------------------------------

    print("\n")
    print("=" * 50)
    print("VISIONRAG EVALUATION SUMMARY")
    print("=" * 50)

    print(
        f"Queries: "
        f"{overall['queries']}"
    )

    print(
        f"Precision@1: "
        f"{overall['precision_at_1']:.3f}"
    )

    print(
        f"Precision@3: "
        f"{overall['precision_at_3']:.3f}"
    )

    print(
        f"Precision@5: "
        f"{overall['precision_at_5']:.3f}"
    )

    print(
        f"Recall@5: "
        f"{overall['recall_at_5']:.3f}"
    )

    print(
        f"Average Similarity: "
        f"{overall['average_similarity']:.3f}"
    )

    print("=" * 50)

    print(
        f"\nResults saved to:\n"
        f"{RESULTS_PATH}"
    )


if __name__ == "__main__":
    main()