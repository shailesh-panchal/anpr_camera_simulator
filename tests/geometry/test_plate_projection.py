import pytest

from anpr_simulator.geometry.camera_intrinsics import (
    CameraIntrinsics,
)

from anpr_simulator.geometry.license_plate import (
    LicensePlateDimensions,
)

from anpr_simulator.geometry.plate_projection import (
    ProjectedPlate,
    project_plate,
)


def test_project_plate():

    intrinsics = CameraIntrinsics(
        fx=973.4,
        fy=983.4,
        cx=968.0,
        cy=550.0,
    )

    plate = LicensePlateDimensions(
        width_m=0.52,
        height_m=0.11,
    )

    result = project_plate(
        center_x_m=0.0,
        center_y_m=0.0,
        distance_z_m=50.0,
        dimensions=plate,
        intrinsics=intrinsics,
    )

    assert isinstance(result, ProjectedPlate)

    expected_width = (
        973.4 * 0.52 / 50.0
    )

    expected_height = (
        983.4 * 0.11 / 50.0
    )

    assert result.width_pixels == pytest.approx(
        expected_width
    )

    assert result.height_pixels == pytest.approx(
        expected_height
    )

def test_plate_size_decreases_with_distance():

    intrinsics = CameraIntrinsics(
        fx=973.4,
        fy=983.4,
        cx=968.0,
        cy=550.0,
    )

    plate = LicensePlateDimensions(
        width_m=0.52,
        height_m=0.11,
    )

    near_plate = project_plate(
        center_x_m=0.0,
        center_y_m=0.0,
        distance_z_m=25.0,
        dimensions=plate,
        intrinsics=intrinsics,
    )

    far_plate = project_plate(
        center_x_m=0.0,
        center_y_m=0.0,
        distance_z_m=50.0,
        dimensions=plate,
        intrinsics=intrinsics,
    )

    assert near_plate.width_pixels > far_plate.width_pixels
    assert near_plate.height_pixels > far_plate.height_pixels