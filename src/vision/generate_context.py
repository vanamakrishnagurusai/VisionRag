from pathlib import Path
import json


from src.vision.context_generator import (
    generate_visual_context
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

METADATA_DIR = (
    PROJECT_ROOT
    / "data"
    / "metadata"
)

INPUT_FILE = (
    METADATA_DIR
    / "detections.json"
)

OUTPUT_FILE = (
    METADATA_DIR
    / "visual_context.json"
)


def generate_context():

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        image_data = json.load(f)

    results = []

    for image in image_data:

        context = generate_visual_context(
            image
        )

        image["visual_context"] = context

        results.append(image)

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            results,
            f,
            indent=4
        )

    print(
        f"Generated context for "
        f"{len(results)} images."
    )

    print(
        f"Saved to:\n{OUTPUT_FILE}"
    )


if __name__ == "__main__":
    generate_context()