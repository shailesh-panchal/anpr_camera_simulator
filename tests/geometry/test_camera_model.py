import pytest
import math

from anpr_simulator.geometry.camera_model import (
    focal_length_pixels,
    horizontal_fov_deg,
    vertical_fov_deg,
)

ACTIVE_PIXEL_WIDTH = 1936
ACTIVE_AREA_WIDTH_MM = 5.57


def test_focal_length_pixels_at_wide():

    result = focal_length_pixels(
        focal_length_mm=2.8,
        active_pixels_width=ACTIVE_PIXEL_WIDTH,
        active_area_width_mm=ACTIVE_AREA_WIDTH_MM,
    )

    expected = 2.8 * 1936 / 5.57

    assert result == pytest.approx(expected)


def test_focal_length_pixels_at_tele():

    result = focal_length_pixels(
        focal_length_mm=12.0,
        active_pixels_width=ACTIVE_PIXEL_WIDTH,
        active_area_width_mm=ACTIVE_AREA_WIDTH_MM,
    )

    expected = 12.0 * 1936 / 5.57

    assert result == pytest.approx(expected)


def test_invalid_focal_length():

    with pytest.raises(ValueError):

        focal_length_pixels(
            focal_length_mm=0,
            active_pixels_width=1936,
            active_area_width_mm=5.57,
        )


def test_invalid_active_pixel_width():

    with pytest.raises(ValueError):

        focal_length_pixels(
            focal_length_mm=2.8,
            active_pixels_width=0,
            active_area_width_mm=5.57,
        )


def test_invalid_active_area_width():

    with pytest.raises(ValueError):

        focal_length_pixels(
            focal_length_mm=2.8,
            active_pixels_width=1936,
            active_area_width_mm=0,
        )

def test_horizontal_fov_at_wide():

    result = horizontal_fov_deg(
        focal_length_mm=2.8,
        active_area_width_mm=5.57,
    )

    expected = math.degrees(
        2.0 * math.atan(
            5.57 / (2.0 * 2.8)
        )
    )

    assert result == pytest.approx(expected)


def test_horizontal_fov_at_tele():

    result = horizontal_fov_deg(
        focal_length_mm=12.0,
        active_area_width_mm=5.57,
    )

    expected = math.degrees(
        2.0 * math.atan(
            5.57 / (2.0 * 12.0)
        )
    )

    assert result == pytest.approx(expected)

def test_vertical_fov_at_wide():

    result = vertical_fov_deg(
        focal_length_mm=2.8,
        active_area_height_mm=3.13,
    )

    expected = math.degrees(
        2.0 * math.atan(
            3.13 / (2.0 * 2.8)
        )
    )

    assert result == pytest.approx(expected)


def test_vertical_fov_at_tele():

    result = vertical_fov_deg(
        focal_length_mm=12.0,
        active_area_height_mm=3.13,
    )

    expected = math.degrees(
        2.0 * math.atan(
            3.13 / (2.0 * 12.0)
        )
    )

    assert result == pytest.approx(expected)