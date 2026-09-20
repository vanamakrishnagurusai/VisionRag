from pathlib import Path

from src.vision.captioner import ImageCaptioner
from src.ingestion.image_loader import get_image_paths


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DIR = (
    PROJECT_ROOT
    / "data"
    / "raw"
)


def main():

    image_paths = get_image_paths(
        RAW_DIR
    )

    if not image_paths:

        print(
            "No images found in data/raw/"
        )

        return

    image_path = image_paths[0]

    print(
        f"\nTesting image: {image_path.name}"
    )

    captioner = ImageCaptioner()

    caption = captioner.generate_caption(
        str(image_path)
    )

    print(
        "\nGenerated caption:"
    )

    print(caption)


if __name__ == "__main__":
    main()