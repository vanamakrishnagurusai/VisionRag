from collections import Counter

from src.vision.spatial import get_position


def generate_visual_context(image_data):

    objects = image_data.get("objects", [])

    image_width = image_data.get(
        "width",
        1
    )

    image_height = image_data.get(
        "height",
        1
    )

    if not objects:

        return (
            "No recognizable objects were detected "
            "in this image."
        )

    labels = [
        obj["class"]
        for obj in objects
    ]

    counts = Counter(labels)

    # ------------------------------------------
    # Object summary
    # ------------------------------------------

    object_parts = []

    for label, count in counts.items():

        if count == 1:
            object_parts.append(
                f"one {label}"
            )
        else:
            object_parts.append(
                f"{count} {label}s"
            )

    object_description = ", ".join(
        object_parts
    )

    # ------------------------------------------
    # Spatial descriptions
    # ------------------------------------------

    spatial_objects = []

    for obj in objects:

        position = get_position(
            obj["bbox"],
            image_width,
            image_height
        )

        spatial_objects.append(
            f"{obj['class']} at {position}"
        )

    spatial_description = ", ".join(
        spatial_objects
    )

    # ------------------------------------------
    # Final searchable context
    # ------------------------------------------

    context = (
        f"Visual scene containing "
        f"{object_description}. "
        f"Detected objects include "
        f"{', '.join(sorted(counts.keys()))}. "
        f"Object positions: "
        f"{spatial_description}."
    )

    return context