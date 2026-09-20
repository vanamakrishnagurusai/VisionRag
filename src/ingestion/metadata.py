from pathlib import Path
import json
import cv2

from src.ingestion.image_loader import get_image_paths, load_image


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DIR = PROJECT_ROOT / "data" / "raw"
METADATA_DIR = PROJECT_ROOT / "data" / "metadata"


def generate_metadata():

    METADATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    image_paths = get_image_paths(RAW_DIR)

    metadata = []

    for index, image_path in enumerate(image_paths):

        image = load_image(image_path)

        height, width = image.shape[:2]

        record = {
            "image_id": index,
            "filename": image_path.name,
            "filepath": str(image_path),
            "width": width,
            "height": height
        }

        metadata.append(record)

    output_file = METADATA_DIR / "images.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(
            metadata,
            f,
            indent=4
        )

    print(
        f"Saved metadata for {len(metadata)} images."
    )


if __name__ == "__main__":
    generate_metadata()