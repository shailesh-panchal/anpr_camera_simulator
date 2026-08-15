import pytest

from anpr_simulator.geometry.camera_intrinsics import (
    CameraIntrinsics,
    create_camera_intrinsics,
)


ACTIVE_WIDTH = 1936
ACTIVE_HEIGHT = 1100

ACTIVE_AREA_WIDTH_MM = 5.57
ACTIVE_AREA_HEIGHT_MM = 3.13


def test_camera_intrinsics_at_wide():

    result = create_camera_intrinsics(
        focal_length_mm=2.8,
        active_pixel_width=ACTIVE_WIDTH,
        active_pixel_height=ACTIVE_HEIGHT,
        active_area_width_mm=ACTIVE_AREA_WIDTH_MM,
        active_area_height_mm=ACTIVE_AREA_HEIGHT_MM,
    )

    assert isinstance(result, CameraIntrinsics)

    assert result.fx == pytest.approx(
        2.8 * 1936 / 5.57
    )

    assert result.fy == pytest.approx(
        2.8 * 1100 / 3.13
    )

    assert result.cx == pytest.approx(968.0)

    assert result.cy == pytest.approx(550.0)


def test_camera_intrinsics_at_tele():

    result = create_camera_intrinsics(
        focal_length_mm=12.0,
        active_pixel_width=ACTIVE_WIDTH,
        active_pixel_height=ACTIVE_HEIGHT,
        active_area_width_mm=ACTIVE_AREA_WIDTH_MM,
        active_area_height_mm=ACTIVE_AREA_HEIGHT_MM,
    )

    assert result.fx == pytest.approx(
        12.0 * 1936 / 5.57
    )

    assert result.fy == pytest.approx(
        12.0 * 1100 / 3.13
    )

    assert result.cx == pytest.approx(968.0)

    assert result.cy == pytest.approx(550.0)