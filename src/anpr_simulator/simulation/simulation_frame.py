from dataclasses import dataclass

from anpr_simulator.geometry.plate_projection import (
    ProjectedPlate,
)
from anpr_simulator.geometry.vehicle_state import (
    VehicleState,
)


@dataclass(frozen=True)
class SimulationFrame:
    """
    Represents the simulated state of one video frame.
    """

    frame_number: int
    timestamp_s: float
    vehicle_state: VehicleState
    projected_plate: ProjectedPlate

    def __post_init__(self) -> None:

        if self.frame_number < 0:
            raise ValueError(
                "Frame number cannot be negative"
            )

        if self.timestamp_s < 0:
            raise ValueError(
                "Timestamp cannot be negative"
            )