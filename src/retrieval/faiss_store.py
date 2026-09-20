import faiss
import numpy as np


class FAISSStore:

    def __init__(self, dimension):

        self.dimension = dimension

        self.index = faiss.IndexFlatIP(
            dimension
        )

    def add(self, embeddings):

        embeddings = np.asarray(
            embeddings,
            dtype="float32"
        )

        self.index.add(
            embeddings
        )

    def search(
        self,
        query_embedding,
        top_k=5
    ):

        query_embedding = np.asarray(
            query_embedding,
            dtype="float32"
        )

        if query_embedding.ndim == 1:
            query_embedding = query_embedding.reshape(
                1,
                -1
            )

        scores, indices = self.index.search(
            query_embedding,
            top_k
        )

        return scores, indices

    def save(self, path):

        faiss.write_index(
            self.index,
            str(path)
        )

    @classmethod
    def load(cls, path):

        index = faiss.read_index(
            str(path)
        )

        store = cls(
            index.d
        )

        store.index = index

        return store