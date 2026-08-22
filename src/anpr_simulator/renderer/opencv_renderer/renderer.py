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