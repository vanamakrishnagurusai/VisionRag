"""Video processing and frame extraction utilities."""

from pathlib import Path
from typing import List, Union
import cv2
from PIL import Image


class VideoProcessor:
    """Extracts frames and metadata from video files."""

    @staticmethod
    def extract_frames(
        video_path: Union[str, Path],
        frame_rate: int = 1
    ) -> List[Image.Image]:
        """
        Extract frames from a video file at a specified rate (frames per second).

        :param video_path: Path to the video file.
        :param frame_rate: Number of frames to extract per second.
        :return: List of PIL Image frames.
        """
        path = str(video_path)
        cap = cv2.VideoCapture(path)
        if not cap.isOpened():
            raise ValueError(f"Unable to open video file: {video_path}")

        fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
        interval = max(1, int(fps / frame_rate))

        frames = []
        frame_count = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if frame_count % interval == 0:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frames.append(Image.fromarray(rgb_frame))

            frame_count += 1

        cap.release()
        return frames
