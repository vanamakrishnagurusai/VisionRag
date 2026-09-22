from src.retrieval.query_expander import expand_query


def main():

    queries = [
        "person near a car",
        "dog outdoors",
        "cat on a chair",
        "bike near a person"
    ]

    for query in queries:

        print(f"\nOriginal: {query}")

        expanded = expand_query(query)

        for item in expanded:
            print(f"  - {item}")


if __name__ == "__main__":
    main()
