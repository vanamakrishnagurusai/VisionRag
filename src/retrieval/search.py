from pathlib import Path

from src.embeddings.embedder import TextEmbedder
from src.retrieval.faiss_store import FAISSStore


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

        self.embedder = TextEmbedder(
            model_name=model_name
        )

        self.store = FAISSStore.load(
            FAISS_INDEX_PATH
        )

        import json

        with open(
            MAPPING_PATH,
            "r",
            encoding="utf-8"
        ) as file:

            self.mapping = json.load(file)

        print(
            f"Loaded {len(self.mapping)} indexed images."
        )

    # --------------------------------------------------
    # Search
    # --------------------------------------------------

    def search(
        self,
        query,
        top_k=5,
        min_score=0.20,
        object_filter=None
    ):

        if not query or not query.strip():
            return []

        query = query.strip()

        # ----------------------------------------------
        # Create query embedding
        # ----------------------------------------------

        query_embedding = self.embedder.encode(
            [query]
        )

        # ----------------------------------------------
        # Retrieve more results than requested
        # ----------------------------------------------
        #
        # This is important because some results may
        # later be removed by score/object filtering.
        #

        retrieval_k = min(
            max(top_k * 3, 20),
            len(self.mapping)
        )

        scores, indices = self.store.search(
            query_embedding,
            top_k=retrieval_k
        )

        results = []

        # ----------------------------------------------
        # Process FAISS results
        # ----------------------------------------------

        for rank, (score, index) in enumerate(
            zip(scores[0], indices[0]),
            start=1
        ):

            # Invalid FAISS index
            if index < 0:
                continue

            if index >= len(self.mapping):
                continue

            score = float(score)

            item = self.mapping[index]

            # ------------------------------------------
            # Similarity filtering
            # ------------------------------------------

            if score < min_score:
                continue

            # ------------------------------------------
            # Object filtering
            # ------------------------------------------

            if object_filter:

                object_filter_lower = (
                    object_filter.lower()
                )

                objects = item.get(
                    "objects",
                    []
                )

                object_names = [
                    obj.get("class", "").lower()
                    for obj in objects
                ]

                if object_filter_lower not in object_names:
                    continue

            # ------------------------------------------
            # Build result
            # ------------------------------------------

            filename = item.get(
                "filename",
                ""
            )

            results.append(
                {
                    "rank": len(results) + 1,
                    "score": round(score, 4),
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

            # ------------------------------------------
            # Stop once enough results are found
            # ------------------------------------------

            if len(results) >= top_k:
                break

        return results