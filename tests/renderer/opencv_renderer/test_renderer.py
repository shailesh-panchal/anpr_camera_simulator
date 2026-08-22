import cv2
import numpy as np
import cv2

from anpr_simulator.renderer.opencv_renderer.renderer import (
    Resolution,
    create_frame,
    add_background
)

def test_create_frame() :
    resolution = Resolution(
        width= 3840,
        height = 2160,
    )

    frame = create_frame(resolution, 3)
    frame[:] = 0
    assert frame.shape == (2160, 3840, 3)
    assert frame.dtype == np.uint8


def test_add_background() :
    resolution = Resolution(
        width= 3840,
        height = 2160,
    )
    background_color = (40, 50, 60)
    frame = create_frame(resolution, 3)
    add_background(frame,background_color)
    cv2.imshow('frame',frame)
    cv2.waitKey(0)
