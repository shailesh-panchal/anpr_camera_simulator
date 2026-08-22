from dataclasses import dataclass


@dataclass(frozen=True)
class ANPREvaluation:
    """
    Result of applying ANPR criteria to a simulation.
    """

    total_frames: int
    usable_frames: int
    unusable_frames: int

    usable_percentage: float

    first_usable_frame: int | None
    last_usable_frame: int | None

    first_usable_time_s : float | None
    last_usable_time_s : float | None
    capture_window_s : float | None

    maximum_plate_width_pixels: float
    maximum_plate_height_pixels: float

    