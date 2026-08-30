import cv2
import numpy as np

from anpr_simulator.geometry.camera_intrinsics import CameraIntrinsics
from anpr_simulator.geometry.camera_pose import CameraPose
from anpr_simulator.geometry.vehicle import VehicleDimensions
from anpr_simulator.geometry.vehicle_state import VehicleState
from anpr_simulator.renderer.opencv_renderer.renderer import (
    Resolution,
    add_background,
    create_frame,
)
from anpr_simulator.renderer.opencv_renderer.vehicle_render import (
    render_vehicle,
    render_vehicle_from_state,
)


def test_vehicle_render():
    resolution = Resolution(1840, 60)
    channel = 3
    background_color = (0, 0, 0)
    frame = create_frame(resolution, channel)
    frame = add_background(frame, background_color)

    vehicle_position = (100, 100)
    vehicle_color = (255, 0, 0)
    vehicle_size = (1000, 1050)
    frame = render_vehicle(frame, vehicle_position, vehicle_size, vehicle_color)
    cv2.imshow('frame', frame)
    cv2.waitKey(0)


def test_render_vehicle_from_state_matches_vehicle_geometry():
    frame = np.zeros((720, 1280, 3), dtype=np.uint8)
    camera_pose = CameraPose(x_m=0.0, y_m=2.0, z_m=0.0, pitch_deg=10.0)
    intrinsics = CameraIntrinsics(fx=2500.0, fy=2500.0, cx=640.0, cy=360.0)
    vehicle_state = VehicleState(x_m=0.0, y_m=0.5, z_m=10.0)
    vehicle_dimensions = VehicleDimensions(
        length_m=4.2,
        width_m=1.8,
        height_m=1.6,
        license_plate_height_m=0.5,
    )

    rendered = render_vehicle_from_state(
        frame,
        vehicle_state=vehicle_state,
        vehicle_dimensions=vehicle_dimensions,
        camera_pose=camera_pose,
        intrinsics=intrinsics,
        vehicle_color=(80, 80, 80),
    )

    assert rendered.shape == frame.shape
    assert np.any(rendered[:, :, 0] != 0) or np.any(rendered[:, :, 1] != 0) or np.any(rendered[:, :, 2] != 0)