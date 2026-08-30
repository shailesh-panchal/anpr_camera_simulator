import cv2

from anpr_simulator.renderer.opencv_renderer.renderer import (
    Resolution,
    create_frame,
    add_background
)

from anpr_simulator.renderer.opencv_renderer.license_plate_render import  (
    create_license_plate,
    render_license_plate
)

def test_create_license_plate():
    resolution = Resolution(width=1920, height=1080)
    channel = 3
    backgroud_color = (0, 0, 0)
    frame = create_frame(resolution, channel)
    frame = add_background(frame, backgroud_color)

    plate_number = "GJ06LS1234"
    plate_size = (500, 100)
    plate_background_color = (255, 255, 255)
    text_color = (0, 0, 0)

    plate_img = create_license_plate(plate_number,plate_size,plate_background_color,text_color)
    cv2.imshow('plate_img',plate_img)
    cv2.destroyAllWindows()

def test_render_license_plate():
    resolution = Resolution(width=1920, height=1080)
    channel = 3
    backgroud_color = (0, 250, 0)
    frame = create_frame(resolution, channel)
    frame = add_background(frame, backgroud_color)

    plate_number = "GJ06LS1234"
    plate_size = (500, 100)
    plate_background_color = (255, 255, 255)
    text_color = (0, 0, 0)

    plate_img = create_license_plate(plate_number, plate_size, plate_background_color, text_color)

    plate_position = (10, 10)
    plate = render_license_plate(frame, plate_img, plate_position)
    cv2.imshow('plate_img',plate)
    cv2.destroyAllWindows()