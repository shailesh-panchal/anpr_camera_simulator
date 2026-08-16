from dataclasses import dataclass


@dataclass(frozen=True)
class VehicleDimensions:
    """
    Physical dimensions of a vehicle in meters.
    """

    length_m: float
    width_m: float
    height_m: float
    license_plate_height_m: float

    def __post_init__(self) -> None:
        if self.length_m <= 0:
            raise ValueError(
                "Vehicle length must be greater than zero"
            )

        if self.width_m <= 0:
            raise ValueError(
                "Vehicle width must be greater than zero"
            )

        if self.height_m <= 0:
            raise ValueError(
                "Vehicle height must be greater than zero"
            )

        if not (
                0.0
                < self.license_plate_height_m
                < self.height_m
        ):
            raise ValueError(
                "License plate height must be within vehicle height"
            )


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

