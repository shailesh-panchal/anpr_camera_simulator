from dataclasses import dataclass


@dataclass(frozen=True)
class VehicleDimensions:
    """
    Physical dimensions of a vehicle in meters.
    """

    length_m: float
    width_m: float
    height_m: float


@dataclass(frozen=True)
class VehiclePosition:
    """
    Vehicle position in the camera coordinate system.

    x_m:
        Horizontal position relative to camera.

    y_m:
        Vertical position.

    z_m:
        Distance in front of camera.
    """

    x_m: float
    y_m: float
    z_m: float

