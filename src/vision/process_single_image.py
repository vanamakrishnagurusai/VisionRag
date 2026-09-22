import json
from pathlib import Path

import cv2

from src.vision.detector import ObjectDetector
from src.vision.captioner import ImageCaptioner
from src.vision.multimodal_context import generate_multimodal_context


PROJECT_ROOT = Path(__file__).resolve().parents[2]

METADATA_DIR = (
    PROJECT_ROOT
    / "data"
    / "metadata"
)

DETECTIONS_PATH = (
    METADATA_DIR
    / "detections.json"
)

MULTIMODAL_CONTEXT_PATH = (
    METADATA_DIR
    / "multimodal_context.json"
)


SUPPORTED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp"
}


def process_single_image(image_path):

    image_path = Path(image_path)

    if not image_path.exists():
        raise FileNotFoundError(
            f"Image not found: {image_path}"
        )

    if image_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported image format: "
            f"{image_path.suffix}"
        )

    # ----------------------------------------------
    # Read image
    # ----------------------------------------------

    image = cv2.imread(
        str(image_path)
    )

    if image is None:
        raise ValueError(
            f"Could not read image: {image_path}"
        )

    height, width = image.shape[:2]

    # ----------------------------------------------
    # YOLO object detection
    # ----------------------------------------------

    detector = ObjectDetector(
        model_name="yolo11n.pt",
        confidence_threshold=0.40
    )

    detections = detector.detect(
        str(image_path)
    )

    # ----------------------------------------------
    # Generate image caption
    # ----------------------------------------------

    captioner = ImageCaptioner()

    caption = captioner.generate_caption(
        str(image_path)
    )

    # ----------------------------------------------
    # Build image metadata
    # ----------------------------------------------

    image_data = {
        "image_id": image_path.stem,
        "filename": image_path.name,
        "filepath": str(image_path),
        "width": width,
        "height": height,
        "objects": detections
    }

    # ----------------------------------------------
    # Generate multimodal context
    # ----------------------------------------------

    multimodal_context = (
        generate_multimodal_context(
            image_data,
            caption
        )
    )

    # ----------------------------------------------
    # Update detections.json
    # ----------------------------------------------

    METADATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    if DETECTIONS_PATH.exists():

        with open(
            DETECTIONS_PATH,
            "r",
            encoding="utf-8"
        ) as file:

            detections_data = json.load(file)

    else:

        detections_data = []

    # Remove existing record for same image
    detections_data = [
        item
        for item in detections_data
        if item.get("filename")
        != image_path.name
    ]

    image_data["object_summary"] = {
        obj["class"]: sum(
            1
            for detection in detections
            if detection["class"] == obj["class"]
        )
        for obj in detections
    }

    detections_data.append(
        image_data
    )

    with open(
        DETECTIONS_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            detections_data,
            file,
            indent=2
        )

    # ----------------------------------------------
    # Update multimodal_context.json
    # ----------------------------------------------

    if MULTIMODAL_CONTEXT_PATH.exists():

        with open(
            MULTIMODAL_CONTEXT_PATH,
            "r",
            encoding="utf-8"
        ) as file:

            multimodal_data = json.load(file)

    else:

        multimodal_data = []

    multimodal_data = [
        item
        for item in multimodal_data
        if item.get("filename")
        != image_path.name
    ]

    multimodal_data.append(
        {
            "image_id": image_path.stem,
            "filename": image_path.name,
            "filepath": str(image_path),
            "caption": caption,
            "multimodal_context": multimodal_context,
            "objects": detections
        }
    )

    with open(
        MULTIMODAL_CONTEXT_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            multimodal_data,
            file,
            indent=2
        )

    return {
        "image_id": image_path.stem,
        "filename": image_path.name,
        "filepath": str(image_path),
        "caption": caption,
        "multimodal_context": multimodal_context,
        "objects": detections
    }