from sentence_transformers import SentenceTransformer


class TextEmbedder:

    def __init__(
        self,
        model_name="all-MiniLM-L6-v2"
    ):

        print(
            f"Loading embedding model: {model_name}"
        )

        self.model = SentenceTransformer(
            model_name
        )

    def encode(self, texts):

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        return embeddings