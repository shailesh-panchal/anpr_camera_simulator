import cv2
import numpy as np

from anpr_simulator.renderer.opencv_renderer.renderer import  (
    Resolution,
    create_frame,
    add_background
)
from anpr_simulator.renderer.opencv_renderer.vehicle_render import (
    render_vehicle,
)


def test_vehicle_render():
    resolution = Resolution(1840, 60)
    channel = 3
    background_color = (0, 0, 0)
    frame = create_frame(resolution,channel)
    frame = add_background(frame,background_color)

    vehicle_position = (100,100)
    vehicle_color = (255,0,0)
    vehicle_size = (1000 , 1050)
    frame = render_vehicle(frame, vehicle_position, vehicle_size, vehicle_color)
    cv2.imshow('frame',frame)
    cv2.waitKey(0)