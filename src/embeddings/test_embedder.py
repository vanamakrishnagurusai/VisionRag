from src.embeddings.embedder import TextEmbedder


def main():

    embedder = TextEmbedder()

    texts = [
        "A person standing near a car.",
        "A vehicle with a person nearby.",
        "A dog running in a park."
    ]

    embeddings = embedder.encode(texts)

    print(
        "Embedding shape:",
        embeddings.shape
    )

    print(
        "First embedding:"
    )

    print(
        embeddings[0]
    )


if __name__ == "__main__":
    main()