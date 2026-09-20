
from pathlib import Path
import cv2

from src.retrieval.search import ImageSearcher


def draw_detections(image, objects):
    """
    Draw YOLO bounding boxes and labels
    on the retrieved image.
    """

    for obj in objects:

        bbox = obj.get("bbox")

        if not bbox or len(bbox) != 4:
            continue

        x1, y1, x2, y2 = map(
            int,
            bbox
        )

        class_name = obj.get(
            "class",
            "object"
        )

        confidence = obj.get(
            "confidence",
            0.0
        )

        label = (
            f"{class_name} "
            f"{confidence:.2f}"
        )

        # Draw bounding box
        cv2.rectangle(
            image,
            (x1, y1),
            (x2, y2),
            (255, 255, 255),
            2
        )

        # Draw label background
        (text_width, text_height), baseline = (
            cv2.getTextSize(
                label,
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                2
            )
        )

        label_y = max(
            y1,
            text_height + baseline
        )

        cv2.rectangle(
            image,
            (
                x1,
                label_y - text_height - baseline
            ),
            (
                x1 + text_width,
                label_y
            ),
            (255, 255, 255),
            -1
        )

        # Draw label text
        cv2.putText(
            image,
            label,
            (
                x1,
                label_y - baseline
            ),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 0, 0),
            2
        )

    return image


def display_result(result):
    """
    Load and display one search result.
    """

    image_path = Path(
        result["filepath"]
    )

    image = cv2.imread(
        str(image_path)
    )

    if image is None:

        print(
            f"Could not load image: "
            f"{image_path}"
        )

        return

    # Draw YOLO detections
    image = draw_detections(
        image,
        result.get("objects", [])
    )

    # Add retrieval information
    header = (
        f"#{result['rank']} "
        f"{result['filename']} | "
        f"Score: {result['score']:.3f}"
    )

    cv2.putText(
        image,
        header,
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    window_name = (
        f"Result #{result['rank']} - "
        f"{result['filename']}"
    )

    cv2.imshow(
        window_name,
        image
    )


def display_results(
    query,
    results
):
    """
    Display all retrieved images.
    """

    if not results:

        print(
            "\nNo relevant images found."
        )

        return

    print(
        "\n" + "=" * 70
    )

    print(
        f"QUERY: {query}"
    )

    print(
        "=" * 70
    )

    for result in results:

        print(
            f"\n#{result['rank']} "
            f"{result['filename']}"
        )

        print(
            f"Similarity Score: "
            f"{result['score']:.4f}"
        )

        print(
            f"Caption: "
            f"{result.get('caption', 'N/A')}"
        )

        objects = [
            obj.get("class", "unknown")
            for obj in result.get(
                "objects",
                []
            )
        ]

        if objects:

            print(
                "Objects: "
                + ", ".join(objects)
            )

        else:

            print(
                "Objects: None"
            )

        print(
            f"Path: "
            f"{result['filepath']}"
        )

        display_result(result)

    print(
        "\nPress any key in an image window "
        "to close the results."
    )

    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main():

    print(
        "\n========================================"
    )

    print(
        "        VisionRAG Visual Search"
    )

    print(
        "========================================"
    )

    searcher = ImageSearcher()

    while True:

        query = input(
            "\nEnter search query "
            "(or 'exit' to quit): "
        ).strip()

        if query.lower() == "exit":

            print(
                "Exiting VisionRAG."
            )

            break

        if not query:

            print(
                "Please enter a search query."
            )

            continue

        try:

            top_k_input = input(
                "Number of results [5]: "
            ).strip()

            if top_k_input:

                top_k = int(
                    top_k_input
                )

                if top_k <= 0:

                    print(
                        "top_k must be greater than 0."
                    )

                    continue

            else:

                top_k = 5

        except ValueError:

            print(
                "Invalid number. "
                "Using top_k=5."
            )

            top_k = 5

        print(
            "\nSearching..."
        )

        try:

            results = searcher.search(
                query,
                top_k=top_k
            )

            display_results(
                query,
                results
            )

        except Exception as error:

            print(
                "\nSearch failed:"
            )

            print(error)


if __name__ == "__main__":
    main()

