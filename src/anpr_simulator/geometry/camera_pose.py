from dataclasses import dataclass


@dataclass(frozen=True)
class CameraPose:
    """
    Camera position and orientation in the world.

    x_m:
        Camera lateral position.

    y_m:
        Camera height above the road.

    z_m:
        Camera position along the road.

    pitch_deg:
        Camera pitch angle in degrees.

    Camera pose in world coordinates.

    Coordinate system:

        X → lateral
        Y → upward
        Z → forward along road

    pitch_deg:

        Positive value means the camera is
        pitched downward toward the road.
    """

    x_m: float
    y_m: float
    z_m: float
    pitch_deg: float

    def __post_init__(self) -> None:
        if self.y_m < 0:
            raise ValueError(
                "Camera height cannot be negative"
            )

        if not -90.0 < self.pitch_deg < 90.0:
            raise ValueError(
                "Camera pitch must be between -90 and 90 degrees"
            )