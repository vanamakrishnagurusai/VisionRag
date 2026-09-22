from pathlib import Path

from src.vision.process_single_image import process_single_image


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DIR = (
    PROJECT_ROOT
    / "data"
    / "raw"
)


def main():

    images = list(
        RAW_DIR.glob("*.jpg")
    )

    if not images:
        images = list(
            RAW_DIR.glob("*.png")
        )

    if not images:
        print(
            "No test images found in data/raw/"
        )
        return

    image_path = images[0]

    print(
        f"Processing: {image_path.name}"
    )

    result = process_single_image(
        image_path
    )

    print("\nProcessing complete.")

    print(
        f"Filename: {result['filename']}"
    )

    print(
        f"Caption: {result['caption']}"
    )

    print(
        f"Objects: {result['objects']}"
    )

    print(
        "\nMultimodal context:"
    )

    print(
        result["multimodal_context"]
    )


if __name__ == "__main__":
    main()