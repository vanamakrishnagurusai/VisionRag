import json
from pathlib import Path
from collections import defaultdict


PROJECT_ROOT = Path(__file__).resolve().parents[2]

METADATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "metadata"
    / "multimodal_context.json"
)

OUTPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "evaluation"
    / "queries.json"
)


# Object categories with enough examples
# to make useful evaluation queries.
TARGET_OBJECTS = [
    "person",
    "chair",
    "bowl",
    "elephant",
    "donut",
    "bird",
    "carrot",
    "giraffe",
    "car",
    "cup",
    "bottle",
    "dog",
    "clock",
    "dining table",
    "pizza",
    "teddy bear",
    "umbrella",
    "motorcycle",
    "airplane",
    "cake",
    "couch",
    "frisbee",
    "zebra",
    "bus",
    "cat",
    "truck",
    "bicycle",
    "book",
    "suitcase",
    "hot dog",
]


def main():

    with open(
        METADATA_PATH,
        "r",
        encoding="utf-8"
    ) as file:
        metadata = json.load(file)

    object_images = defaultdict(set)

    for item in metadata:

        filename = item.get("filename")

        if not filename:
            continue

        for obj in item.get("objects", []):

            label = obj.get("class")

            if label:
                object_images[label].add(filename)

    evaluation_queries = []

    for object_name in TARGET_OBJECTS:

        filenames = sorted(
            object_images.get(object_name, set())
        )

        if not filenames:
            continue

        evaluation_queries.append(
            {
                "query": f"images containing a {object_name}",
                "relevant_images": filenames
            }
        )

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        OUTPUT_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            evaluation_queries,
            file,
            indent=2
        )

    print(
        f"Created {len(evaluation_queries)} evaluation queries."
    )

    print(
        f"Output: {OUTPUT_PATH}"
    )

    print("\nEvaluation queries:")

    for item in evaluation_queries:

        print(
            f"- {item['query']}: "
            f"{len(item['relevant_images'])} relevant images"
        )


if __name__ == "__main__":
    main()