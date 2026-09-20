from pathlib import Path

from ultralytics import YOLO


class ObjectDetector:

    def __init__(
        self,
        model_name="yolo11n.pt",
        confidence_threshold=0.40
    ):
        self.model = YOLO(model_name)
        self.confidence_threshold = confidence_threshold

    def detect(self, image_path: str):

        results = self.model.predict(
            source=image_path,
            conf=self.confidence_threshold,
            verbose=False
        )

        result = results[0]

        detections = []

        names = result.names

        if result.boxes is None:
            return detections

        for box in result.boxes:

            class_id = int(box.cls[0])
            confidence = float(box.conf[0])

            x1, y1, x2, y2 = (
                box.xyxy[0].tolist()
            )

            detection = {
                "class": names[class_id],
                "class_id": class_id,
                "confidence": round(confidence, 4),
                "bbox": [
                    round(x1, 2),
                    round(y1, 2),
                    round(x2, 2),
                    round(y2, 2)
                ]
            }

            detections.append(detection)

        return detections

def get_object_summary(detections):

    object_counts = {}

    for detection in detections:

        label = detection["class"]

        object_counts[label] = (
            object_counts.get(label, 0) + 1
        )

    return object_counts