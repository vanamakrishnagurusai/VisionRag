OBJECT_SYNONYMS = {
    "car": [
        "car",
        "automobile",
        "vehicle"
    ],
    "person": [
        "person",
        "people",
        "human",
        "man",
        "woman"
    ],
    "dog": [
        "dog",
        "puppy",
        "canine"
    ],
    "cat": [
        "cat",
        "kitten",
        "feline"
    ],
    "bike": [
        "bike",
        "bicycle",
        "cycle"
    ],
    "motorcycle": [
        "motorcycle",
        "motorbike"
    ],
    "bus": [
        "bus",
        "coach"
    ],
    "truck": [
        "truck",
        "lorry"
    ],
    "bird": [
        "bird",
        "avian"
    ]
}


def expand_query(query):

    query = query.strip().lower()

    expanded_queries = [query]

    for category, synonyms in OBJECT_SYNONYMS.items():

        if category in query:

            for synonym in synonyms:

                expanded_query = query.replace(
                    category,
                    synonym
                )

                if expanded_query not in expanded_queries:
                    expanded_queries.append(
                        expanded_query
                    )

    return expanded_queries