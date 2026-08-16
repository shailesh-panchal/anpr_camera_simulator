from dataclasses import dataclass


from anpr_simulator.geometry.vehicle import (
    VehicleDimensions,
)
from anpr_simulator.geometry.vehicle_trajectory import (
    VehicleTrajectory,
)


@dataclass(frozen=True)
class VehicleState:
    x_m: float
    y_m: float
    z_m: float


def vehicle_state_at_time(
    trajectory: VehicleTrajectory,
    dimensions: VehicleDimensions,
    time_s: float,
) -> VehicleState:

    x_m, _, z_m = trajectory.position_at_time(
        time_s
    )

    return VehicleState(
        x_m=x_m,
        y_m=dimensions.license_plate_height_m,
        z_m=z_m,
    )