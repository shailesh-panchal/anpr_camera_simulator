from dataclasses import dataclass


@dataclass(frozen=True)
class SimulationResult:
    """Summary of one completed simulation."""

    scenario_name: str

    total_frames: int

    first_frame_number: int
    last_frame_number: int

    maximum_plate_width_pixels: float
    minimum_plate_width_pixels: float

    maximum_plate_height_pixels: float
    minimum_plate_height_pixels: float

    maximum_plate_distance_m: float
    minimum_plate_distance_m: float