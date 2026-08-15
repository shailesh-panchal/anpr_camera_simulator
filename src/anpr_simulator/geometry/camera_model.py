import math

def focal_length_pixels(
    focal_length_mm: float,
    active_pixels: int,
    active_area_mm: float,
) -> float:
    """
    Calculate focal length in pixels.

    Args:
        focal_length_mm:
            Physical lens focal length in millimeters.

        active_pixels:
            Number of active pixels across the sensor width.

        active_area_mm:
            Physical width of the active sensor area in millimeters.

    Returns:
        Focal length expressed in pixels.

    Raises:
        ValueError:
            If any input parameter is invalid.
    """

    if focal_length_mm <= 0:
        raise ValueError(
            "Focal length must be greater than 0"
        )

    if active_pixels <= 0:
        raise ValueError(
            "Active pixel width must be greater than 0"
        )

    if active_area_mm <= 0:
        raise ValueError(
            "Active sensor width must be greater than 0"
        )

    return (
        focal_length_mm
        * active_pixels
        / active_area_mm
    )

def horizontal_fov_deg(
    focal_length_mm: float,
    active_area_width_mm: float,
) -> float:
    """
    Calculate horizontal field of view in degrees.

    Args:
        focal_length_mm:
            Lens focal length in millimeters.

        active_area_width_mm:
            Physical width of the active sensor area in millimeters.

    Returns:
        Horizontal field of view in degrees.

    Raises:
        ValueError:
            If focal length or sensor width is invalid.
    """

    if focal_length_mm <= 0:
        raise ValueError(
            "Focal length must be greater than 0"
        )
    if active_area_width_mm <= 0:
        raise ValueError(
            "Active sensor width must be greater than 0"
        )
    fov_rad = 2.0 * math.atan(
        active_area_width_mm / (2.0 * focal_length_mm)
    )
    return math.degrees(fov_rad)

def vertical_fov_deg(
    focal_length_mm: float,
    active_area_height_mm: float,
) -> float:
    """
    Calculate vertical field of view in degrees.

    Args:
        focal_length_mm:
            Lens focal length in millimeters.

        active_area_height_mm:
            Physical height of the active sensor area
            in millimeters.

    Returns:
        Vertical field of view in degrees.

    Raises:
        ValueError:
            If focal length or sensor height is invalid.
    """

    if focal_length_mm <= 0:
        raise ValueError(
            "Focal length must be greater than 0"
        )
    if active_area_height_mm <= 0:
        raise ValueError(
            "Active sensor height must be greater than 0"
        )
    fov_rad = 2.0 * math.atan(
        active_area_height_mm / (2.0 * focal_length_mm)
    )
    return math.degrees(fov_rad)