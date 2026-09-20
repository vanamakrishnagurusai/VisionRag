from pathlib import Path
import json
import cv2

from src.ingestion.image_loader import get_image_paths
from src.vision.detector import (
    ObjectDetector,
    get_object_summary
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DIR = PROJECT_ROOT / "data" / "raw"
METADATA_DIR = PROJECT_ROOT / "data" / "metadata"

OUTPUT_FILE = METADATA_DIR / "detections.json"


def process_detections():

    METADATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    image_paths = get_image_paths(
        RAW_DIR
    )

    detector = ObjectDetector(
        model_name="yolo11n.pt",
        confidence_threshold=0.40
    )

    all_results = []

    print(
        f"Processing {len(image_paths)} images..."
    )

    for image_id, image_path in enumerate(image_paths):

        print(
            f"[{image_id + 1}/{len(image_paths)}] "
            f"{image_path.name}"
        )

        detections = detector.detect(
            str(image_path)
        )

        object_summary = get_object_summary(
            detections
        )
        image = cv2.imread(
            str(image_path)
        )
        height, width = image.shape[:2]

        result = {
            "image_id": image_id,
            "filename": image_path.name,
            "filepath": str(image_path),
            "width": width,
            "height": height,
            "objects": detections,
            "object_summary": object_summary
        }

        all_results.append(result)

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            all_results,
            f,
            indent=4
        )

    print(
        f"\nDetection metadata saved to:"
        f"\n{OUTPUT_FILE}"
    )


if __name__ == "__main__":
    process_detections()