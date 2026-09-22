import json
from pathlib import Path

from src.embeddings.embedder import TextEmbedder
from src.retrieval.faiss_store import FAISSStore
from src.retrieval.query_expander import expand_query


# --------------------------------------------------
# Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

FAISS_INDEX_PATH = (
    PROJECT_ROOT
    / "data"
    / "faiss"
    / "image_index.faiss"
)

MAPPING_PATH = (
    PROJECT_ROOT
    / "data"
    / "faiss"
    / "image_mapping.json"
)


class ImageSearcher:

    def __init__(
        self,
        model_name="all-MiniLM-L6-v2"
    ):

        print("Loading image search system...")

        # ------------------------------------------
        # Embedding model
        # ------------------------------------------

        self.embedder = TextEmbedder(
            model_name=model_name
        )

        # ------------------------------------------
        # FAISS index
        # ------------------------------------------

        self.store = FAISSStore.load(
            FAISS_INDEX_PATH
        )

        # ------------------------------------------
        # Image mapping
        # ------------------------------------------

        with open(
            MAPPING_PATH,
            "r",
            encoding="utf-8"
        ) as file:

            self.mapping = json.load(file)

        print(
            f"Loaded {len(self.mapping)} indexed images."
        )

    # ==================================================
    # Single query search
    # ==================================================

    def _search_single_query(
        self,
        query,
        retrieval_k
    ):

        query_embedding = self.embedder.encode(
            [query]
        )

        scores, indices = self.store.search(
            query_embedding,
            top_k=retrieval_k
        )

        results = []

        for score, index in zip(
            scores[0],
            indices[0]
        ):

            # Invalid FAISS index
            if index < 0:
                continue

            # Mapping safety check
            if index >= len(self.mapping):
                continue

            results.append(
                {
                    "index": int(index),
                    "score": float(score)
                }
            )

        return results

    # ==================================================
    # Main search
    # ==================================================

    def search(
        self,
        query,
        top_k=5,
        min_score=0.20,
        object_filter=None
    ):

        # ------------------------------------------
        # Validate query
        # ------------------------------------------

        if not query or not query.strip():
            return []

        query = query.strip()

        # ------------------------------------------
        # Retrieve more candidates than needed
        # ------------------------------------------

        retrieval_k = min(
            max(top_k * 3, 20),
            len(self.mapping)
        )

        # ------------------------------------------
        # Query expansion
        # ------------------------------------------

        expanded_queries = expand_query(
            query
        )

        print(
            f"Expanded queries: {expanded_queries}"
        )

        # ------------------------------------------
        # Search every expanded query
        # ------------------------------------------

        candidate_scores = {}

        for expanded_query in expanded_queries:

            results = self._search_single_query(
                expanded_query,
                retrieval_k
            )

            for result in results:

                index = result["index"]
                score = result["score"]

                if index not in candidate_scores:
                    candidate_scores[index] = []

                # IMPORTANT:
                # Append outside the if statement.
                candidate_scores[index].append(
                    score
                )

        # ------------------------------------------
        # Score fusion
        # ------------------------------------------

        fused_results = []

        for index, scores in candidate_scores.items():

            # Average score across query variations
            average_score = (
                sum(scores) / len(scores)
            )

            # Small consistency bonus
            consistency_bonus = (
                0.02 * (len(scores) - 1)
            )

            final_score = (
                average_score
                + consistency_bonus
            )

            fused_results.append(
                {
                    "index": index,
                    "score": final_score
                }
            )

        # ------------------------------------------
        # Sort by score
        # ------------------------------------------

        fused_results.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        # ------------------------------------------
        # Build final results
        # ------------------------------------------

        results = []

        for candidate in fused_results:

            index = candidate["index"]
            score = candidate["score"]

            # --------------------------------------
            # Similarity filtering
            # --------------------------------------

            if score < min_score:
                continue

            item = self.mapping[index]

            # --------------------------------------
            # Object filtering
            # --------------------------------------

            if object_filter:

                object_filter_lower = (
                    object_filter.strip().lower()
                )

                objects = item.get(
                    "objects",
                    []
                )

                object_names = [
                    obj.get(
                        "class",
                        ""
                    ).lower()
                    for obj in objects
                ]

                if object_filter_lower not in object_names:
                    continue

            # --------------------------------------
            # Image information
            # --------------------------------------

            filename = item.get(
                "filename",
                ""
            )

            results.append(
                {
                    "rank": len(results) + 1,

                    "score": round(
                        score,
                        4
                    ),

                    "filename": filename,

                    "filepath": item.get(
                        "filepath",
                        ""
                    ),

                    "image_url": (
                        f"/images/{filename}"
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

            # --------------------------------------
            # Stop after top_k valid results
            # --------------------------------------

            if len(results) >= top_k:
                break

        return results