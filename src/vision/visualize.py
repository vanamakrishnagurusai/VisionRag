import cv2
from pathlib import Path

from src.vision.detector import ObjectDetector
from src.ingestion.image_loader import get_image_paths


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DIR = PROJECT_ROOT / "data" / "raw"


def visualize():

    # Find available images
    image_paths = get_image_paths(RAW_DIR)

    if not image_paths:
        print("No images found in data/raw/")
        return

    # Use the first available image
    image_path = image_paths[0]

    print(f"Testing image: {image_path.name}")

    detector = ObjectDetector(
        model_name="yolo11n.pt",
        confidence_threshold=0.40
    )

    results = detector.model.predict(
        source=str(image_path),
        conf=0.40,
        verbose=False
    )

    result = results[0]

    # Draw bounding boxes
    annotated_image = result.plot()

    print("\nDetected objects:")

    if result.boxes is not None:

        for box in result.boxes:

            class_id = int(box.cls[0])
            confidence = float(box.conf[0])

            class_name = result.names[class_id]

            print(
                f"- {class_name}: "
                f"{confidence:.2f}"
            )

    else:
        print("No objects detected.")

    # Display result
    cv2.imshow(
        "VisionRAG - Object Detection",
        annotated_image
    )

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    visualize()