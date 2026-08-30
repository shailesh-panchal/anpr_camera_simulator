from dataclasses import dataclass
from enum import Enum


class VehicleDirection(Enum):
    APPROACHING_CAMERA = "approaching_camera"
    MOVING_AWAY = "moving_away"


@dataclass(frozen=True)
class VehicleTrajectory:
    """
    Describes a vehicle moving along the road.
    """

    initial_z_m: float
    speed_mps: float
    x_m: float
    y_m: float
    direction: VehicleDirection

    def position_at_time(
        self,
        time_s: float,
    ) -> tuple[float, float, float]:

        if time_s < 0:
            raise ValueError(
                "Time must be greater than or equal to 0"
            )

        if self.speed_mps < 0:
            raise ValueError(
                "Speed cannot be negative"
            )

        if self.initial_z_m < 0:
            raise ValueError(
                "Initial distance cannot be negative"
            )

        distance_travelled_m = (
            self.speed_mps * time_s
        )

        if self.direction == VehicleDirection.APPROACHING_CAMERA:
            z_m = (
                self.initial_z_m - distance_travelled_m
            )
            if z_m <= 0:
                raise ValueError(
                    "Vehicle has passed the camera"
                )
        else:
            z_m = (
                self.initial_z_m + distance_travelled_m
            )

        return (
            self.x_m,
            self.y_m,
            z_m,
        )

