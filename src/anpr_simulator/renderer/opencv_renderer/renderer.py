from dataclasses import dataclass

import cv2
import numpy as np

@dataclass
class Resolution:
    width: int
    height: int

    def __post_init__(self) -> None:

        if self.width <= 0 or self.height <= 0:
            raise ValueError("Width and height must not be zero")
        self.width = int(self.width)
        self.height = int(self.height)

def create_frame(resolution : Resolution, channel : int) -> np.ndarray :
    frame = np.zeros((resolution.height, resolution.width, channel), dtype=np.uint8)
    return frame


def add_background(frame : np.ndarray, background_color: tuple[int, int, int]) -> np.ndarray :
    frame[:] = background_color
    return frame


def add_road_background(
    frame: np.ndarray,
    sky_color: tuple[int, int, int] = (25, 30, 35),
    road_color: tuple[int, int, int] = (45, 45, 45),
    lane_color: tuple[int, int, int] = (220, 220, 220),
    horizon_y_ratio: float = 0.62,
) -> np.ndarray:
    """
    Paint a simple road scene: sky above the horizon, road below, and a central lane line.
    """
    if frame is None or not isinstance(frame, np.ndarray):
        raise ValueError("frame must be a numpy ndarray")

    if frame.ndim != 3 or frame.shape[2] != 3:
        raise ValueError("frame must be a 3-channel image array")

    height, width, _ = frame.shape
    horizon_y = int(height * horizon_y_ratio)

    frame[:horizon_y] = sky_color
    frame[horizon_y:] = road_color

    road_left = int(width * 0.15)
    road_right = int(width * 0.85)
    for y in range(horizon_y, height):
        frame[y, road_left:road_left + 2] = (90, 90, 90)
        frame[y, road_right:road_right + 2] = (90, 90, 90)

    center_x = width // 2
    for y in range(horizon_y, height, 10):
        cv2.line(frame, (center_x - 2, y), (center_x + 2, y), lane_color, 2)

    return frame