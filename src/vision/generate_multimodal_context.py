from pathlib import Path
import json

from src.vision.captioner import ImageCaptioner
from src.vision.multimodal_context import (
    generate_multimodal_context
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
    / "multimodal_context.json"
)


def main():

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        image_data = json.load(f)

    captioner = ImageCaptioner()

    results = []

    print(
        f"Processing {len(image_data)} images..."
    )

    for index, item in enumerate(
        image_data
    ):

        print(
            f"[{index + 1}/{len(image_data)}] "
            f"{item['filename']}"
        )

        caption = (
            captioner.generate_caption(
                item["filepath"]
            )
        )

        context = (
            generate_multimodal_context(
                item,
                caption
            )
        )

        item["caption"] = caption

        item[
            "multimodal_context"
        ] = context

        results.append(item)

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
        "\nMultimodal metadata saved to:"
    )

    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()