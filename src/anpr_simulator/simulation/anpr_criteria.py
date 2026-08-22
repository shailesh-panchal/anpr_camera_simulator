from dataclasses import dataclass


@dataclass(frozen=True)
class ANPRCriteria:
    """
    Defines the minimum license-plate image requirements
    for considering a frame usable for ANPR.
    """

    minimum_plate_width_pixels: float
    minimum_plate_height_pixels: float

    def __post_init__(self) -> None:

        if self.minimum_plate_width_pixels <= 0:
            raise ValueError(
                "Minimum plate width must be greater than zero"
            )

        if self.minimum_plate_height_pixels <= 0:
            raise ValueError(
                "Minimum plate height must be greater than zero"
            )

