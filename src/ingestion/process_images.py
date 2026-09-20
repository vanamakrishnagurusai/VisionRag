from pathlib import Path
import cv2

from src.ingestion.image_loader import get_image_paths, load_image


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


def process_images():

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    image_paths = get_image_paths(RAW_DIR)

    print(f"Found {len(image_paths)} images.")

    for image_path in image_paths:

        image = load_image(image_path)

        height, width = image.shape[:2]

        print(
            f"{image_path.name} "
            f"-> {width}x{height}"
        )

        output_path = PROCESSED_DIR / image_path.name

        cv2.imwrite(
            str(output_path),
            image
        )

    print("Image processing completed.")


if __name__ == "__main__":
    process_images()