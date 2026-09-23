import re


OBJECT_SYNONYMS = {
    "car": ["car", "automobile", "vehicle"],
    "person": ["person", "people", "human", "man", "woman"],
    "dog": ["dog", "puppy", "canine"],
    "cat": ["cat", "kitten", "feline"],
    "bike": ["bike", "bicycle", "cycle"],
    "motorcycle": ["motorcycle", "motorbike"],
    "bus": ["bus", "coach"],
    "truck": ["truck", "lorry"],
    "bird": ["bird", "avian"],
}


def expand_query(query):
    query = query.strip().lower()

    expanded_queries = [query]

    for category, synonyms in OBJECT_SYNONYMS.items():

        # Match the complete word only.
        pattern = rf"\b{re.escape(category)}\b"

        if not re.search(pattern, query):
            continue

        for synonym in synonyms:

            expanded_query = re.sub(
                pattern,
                synonym,
                query
            )

            if expanded_query not in expanded_queries:
                expanded_queries.append(
                    expanded_query
                )

    return expanded_queries