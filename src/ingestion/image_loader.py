from pathlib import Path
import cv2


SUPPORTED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp"
}


def get_image_paths(directory: str):
    """
    Return all supported image paths from a directory.
    """

    directory = Path(directory)

    if not directory.exists():
        raise FileNotFoundError(
            f"Directory does not exist: {directory}"
        )

    image_paths = []

    for path in directory.iterdir():

        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
            image_paths.append(path)

    return sorted(image_paths)


def load_image(path: Path):
    """
    Load an image using OpenCV.
    """

    image = cv2.imread(str(path))

    if image is None:
        raise ValueError(
            f"Unable to read image: {path}"
        )

    return image