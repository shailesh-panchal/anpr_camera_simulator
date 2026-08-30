from anpr_simulator.geometry.camera_intrinsics import (
    CameraIntrinsics,
)
from anpr_simulator.geometry.camera_pose import (
    CameraPose,
)
from anpr_simulator.geometry.license_plate import (
    LicensePlateDimensions,
)
from anpr_simulator.geometry.vehicle import (
    VehicleDimensions,
)
from anpr_simulator.geometry.vehicle_trajectory import (
    VehicleDirection,
    VehicleTrajectory,
)
from anpr_simulator.simulation.frame_generator import (
    FrameGenerator,
)
from anpr_simulator.simulation.simulation_frame import (
    SimulationFrame,
)


def create_test_generator() -> FrameGenerator:

    intrinsics = CameraIntrinsics(
        fx=973.4,
        fy=983.4,
        cx=968.0,
        cy=550.0,
    )

    camera_pose = CameraPose(
        x_m=0.0,
        y_m=5.0,
        z_m=0.0,
        pitch_deg=0.0,
    )

    vehicle = VehicleDimensions(
        length_m=4.5,
        width_m=1.8,
        height_m=1.5,
        license_plate_height_m=0.5,
    )

    plate = LicensePlateDimensions(
        width_m=0.52,
        height_m=0.11,
    )

    trajectory = VehicleTrajectory(
        initial_z_m=100.0,
        speed_mps=10.0,
        x_m=0.0,
        y_m=0.0,
        direction=VehicleDirection.APPROACHING_CAMERA,
    )

    return FrameGenerator(
        fps=10.0,
        duration_s=1.0,
        trajectory=trajectory,
        vehicle_dimensions=vehicle,
        plate_dimensions=plate,
        camera_pose=camera_pose,
        intrinsics=intrinsics,
    )

import numpy as np
import pytest

from anpr_simulator.geometry.camera_intrinsics import (
    CameraIntrinsics,
)
from anpr_simulator.geometry.camera_pose import (
    CameraPose,
)
from anpr_simulator.geometry.license_plate import (
    LicensePlateDimensions,
)
from anpr_simulator.geometry.vehicle import (
    VehicleDimensions,
)
from anpr_simulator.geometry.vehicle_trajectory import (
    VehicleDirection,
    VehicleTrajectory,
)
from anpr_simulator.simulation.frame_generator import (
    FrameGenerator,
)


def create_test_generator_with_input_data(
    fps: float,
    speed_mps: float,
    duration_s: float = 1.0,
) -> FrameGenerator:

    intrinsics = CameraIntrinsics(
        fx=973.4,
        fy=983.4,
        cx=968.0,
        cy=550.0,
    )

    camera_pose = CameraPose(
        x_m=0.0,
        y_m=5.0,
        z_m=0.0,
        pitch_deg=0.0,
    )

    vehicle = VehicleDimensions(
        length_m=4.5,
        width_m=1.8,
        height_m=1.5,
        license_plate_height_m=0.5,
    )

    plate = LicensePlateDimensions(
        width_m=0.52,
        height_m=0.11,
    )

    trajectory = VehicleTrajectory(
        initial_z_m=100.0,
        speed_mps=speed_mps,
        x_m=0.0,
        y_m=0.0,
        direction=VehicleDirection.APPROACHING_CAMERA,
    )

    return FrameGenerator(
        fps=fps,
        duration_s=duration_s,
        trajectory=trajectory,
        vehicle_dimensions=vehicle,
        plate_dimensions=plate,
        camera_pose=camera_pose,
        intrinsics=intrinsics,
    )

def test_frame_generator_count():

    generator = create_test_generator()

    frames = list(generator.generate())

    assert len(frames) == 10

def test_frame_generator_frame_numbers():

    generator = create_test_generator()

    frames = list(generator.generate())

    assert [frame.frame_number for frame in frames] == [
        0,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
    ]

import pytest


def test_frame_generator_timestamps():

    generator = create_test_generator()

    frames = list(generator.generate())

    assert frames[0].timestamp_s == pytest.approx(0.0)
    assert frames[1].timestamp_s == pytest.approx(0.1)
    assert frames[2].timestamp_s == pytest.approx(0.2)
    assert frames[9].timestamp_s == pytest.approx(0.9)


def test_frame_generator_rendered_frames_produce_images():

    generator = create_test_generator()

    rendered_frames = list(
        generator.generate_rendered(
            plate_number="KA01AB1234",
            frame_size=(640, 360),
            vehicle_size=(180, 90),
        )
    )

    assert len(rendered_frames) == 10

    for frame in rendered_frames:
        assert frame.shape == (360, 640, 3)
        assert frame.dtype == np.uint8


def test_vehicle_moves_between_frames():

    generator = create_test_generator()

    frames = list(generator.generate())

    assert frames[0].vehicle_state.z_m == pytest.approx(
        100.0
    )

    assert frames[1].vehicle_state.z_m == pytest.approx(
        99.0
    )

    assert frames[2].vehicle_state.z_m == pytest.approx(
        98.0
    )

@pytest.mark.parametrize(
    "fps",
    [
        10.0,
        15.0,
        25.0,
        30.0,
        50.0,
        60.0,
    ],
)
def test_frame_count_for_different_fps(fps):

    generator = create_test_generator_with_input_data(
        fps=fps,
        speed_mps=10.0,
        duration_s=1.0,
    )

    frames = list(generator.generate())

    assert len(frames) == int(fps)

@pytest.mark.parametrize(
    "speed_mps",
    [
        10.0,
        20.0,
        30.0,
        40.0,
        41.6666667,
    ],
)
def test_vehicle_speed(speed_mps):

    fps = 60.0

    generator = create_test_generator_with_input_data(
        fps=fps,
        speed_mps=speed_mps,
        duration_s=1.0,
    )

    frames = list(generator.generate())

    first_z = frames[0].vehicle_state.z_m
    second_z = frames[1].vehicle_state.z_m

    expected_distance = speed_mps / fps

    actual_distance = first_z - second_z

    assert actual_distance == pytest.approx(
        expected_distance
    )

@pytest.mark.parametrize(
    "fps, speed_mps",
    [
        (10.0, 10.0),
        (10.0, 20.0),
        (10.0, 40.0),

        (30.0, 10.0),
        (30.0, 20.0),
        (30.0, 40.0),

        (60.0, 10.0),
        (60.0, 20.0),
        (60.0, 30.0),
        (60.0, 40.0),
        (60.0, 41.6666667),
    ],
)
def test_fps_and_vehicle_speed(
    fps,
    speed_mps,
):

    generator = create_test_generator_with_input_data(
        fps=fps,
        speed_mps=speed_mps,
        duration_s=1.0,
    )

    frames = list(generator.generate())

    expected_distance_per_frame = (
        speed_mps / fps
    )

    actual_distance_per_frame = (
        frames[0].vehicle_state.z_m
        - frames[1].vehicle_state.z_m
    )

    assert actual_distance_per_frame == pytest.approx(
        expected_distance_per_frame
    )

@pytest.mark.parametrize(
    "fps",
    [
        10.0,
        15.0,
        25.0,
        30.0,
        50.0,
        60.0,
    ],
)
def test_frame_timestamp_interval(fps):

    generator = create_test_generator_with_input_data(
        fps=fps,
        speed_mps=10.0,
        duration_s=1.0,
    )

    frames = list(generator.generate())

    expected_interval = 1.0 / fps

    actual_interval = (
        frames[1].timestamp_s
        - frames[0].timestamp_s
    )

    assert actual_interval == pytest.approx(
        expected_interval
    )

@pytest.mark.parametrize(
    "speed_mps",
    [
        10.0,
        20.0,
        30.0,
        40.0,
        41.6666667,
    ],
)
def test_plate_size_increases_for_approaching_vehicle(
    speed_mps,
):

    generator = create_test_generator_with_input_data(
        fps=60.0,
        speed_mps=speed_mps,
        duration_s=1.0,
    )

    frames = list(generator.generate())

    first_width = (
        frames[0]
        .projected_plate
        .width_pixels
    )

    def test_150_kmh_at_60_fps():
        speed_mps = 150.0 / 3.6
        fps = 60.0

        generator = create_test_generator_with_input_data(
            fps=fps,
            speed_mps=speed_mps,
            duration_s=1.0,
        )

        frames = list(generator.generate())

        assert len(frames) == 60

        expected_distance_per_frame = (
                speed_mps / fps
        )

        actual_distance_per_frame = (
                frames[0].vehicle_state.z_m
                - frames[1].vehicle_state.z_m
        )

        assert actual_distance_per_frame == pytest.approx(
            expected_distance_per_frame
        )

        assert expected_distance_per_frame == pytest.approx(
            0.694444,
            abs=0.001,
        )

    last_width = (
        frames[-1]
        .projected_plate
        .width_pixels
    )

    assert last_width > first_width

@pytest.mark.parametrize(
    "fps",
    [
        10.0,
        30.0,
        60.0,
    ],
)
def test_physical_distance_is_independent_of_fps(fps):

    speed_mps = 10.0

    generator = create_test_generator_with_input_data(
        fps=fps,
        speed_mps=speed_mps,
        duration_s=1.0,
    )

    frames = list(generator.generate())

    initial_z = frames[0].vehicle_state.z_m

    final_z = frames[-1].vehicle_state.z_m

    # Last generated frame is at:
    # (number_of_frames - 1) / FPS
    actual_time = frames[-1].timestamp_s

    expected_z = (
        initial_z
        - speed_mps * actual_time
    )

    assert final_z == pytest.approx(
        expected_z
    )