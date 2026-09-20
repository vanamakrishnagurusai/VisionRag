from collections import Counter

from src.vision.spatial import get_position


def generate_multimodal_context(
    image_data,
    caption
):

    objects = image_data.get(
        "objects",
        []
    )

    image_width = image_data.get(
        "width",
        1
    )

    image_height = image_data.get(
        "height",
        1
    )

    # -----------------------------------------
    # Object information
    # -----------------------------------------

    labels = [
        obj["class"]
        for obj in objects
    ]

    counts = Counter(labels)

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

    object_description = (
        ", ".join(object_parts)
        if object_parts
        else "no recognizable objects"
    )

    # -----------------------------------------
    # Spatial information
    # -----------------------------------------

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

    spatial_description = (
        ", ".join(spatial_objects)
        if spatial_objects
        else "no spatial object information"
    )

    # -----------------------------------------
    # Final multimodal context
    # -----------------------------------------

    context = (
        f"Image caption: {caption}. "
        f"Detected objects: "
        f"{object_description}. "
        f"Object categories: "
        f"{', '.join(sorted(counts.keys())) if counts else 'none'}. "
        f"Object positions: "
        f"{spatial_description}."
    )

    return context