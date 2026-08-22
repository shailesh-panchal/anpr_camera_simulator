from collections.abc import Iterable

from anpr_simulator.simulation.anpr_criteria import (
    ANPRCriteria,
)
from anpr_simulator.simulation.anpr_evaluation import (
    ANPREvaluation,
)
from anpr_simulator.simulation.simulation_frame import (
    SimulationFrame,
)


class ANPREvaluator:
    """
    Evaluates simulation frames against ANPR criteria.

    Frames are processed one at a time, so the evaluator
    does not need to keep all simulation frames in memory.
    """

    def __init__(
        self,
        criteria: ANPRCriteria,
        fps : float,
    ) -> None:

        if fps <= 0:
            raise ValueError("fps must greater than zero"
                             )
        self.criteria = criteria
        self.fps = fps

    def evaluate(
        self,
        frames: Iterable[SimulationFrame],
    ) -> ANPREvaluation:
        """
        Evaluate simulation frames one at a time.
        """

        total_frames = 0
        usable_frames = 0

        first_usable_frame = None
        last_usable_frame = None

        maximum_plate_width_pixels = 0.0
        maximum_plate_height_pixels = 0.0

        for frame in frames:

            total_frames += 1

            plate = frame.projected_plate

            maximum_plate_width_pixels = max(
                maximum_plate_width_pixels,
                plate.width_pixels,
            )

            maximum_plate_height_pixels = max(
                maximum_plate_height_pixels,
                plate.height_pixels,
            )

            is_usable = (
                plate.width_pixels
                >= self.criteria.minimum_plate_width_pixels
                and
                plate.height_pixels
                >= self.criteria.minimum_plate_height_pixels
            )

            if is_usable:

                usable_frames += 1

                if first_usable_frame is None:
                    first_usable_frame = (
                        frame.frame_number
                    )

                last_usable_frame = (
                    frame.frame_number
                )

        if total_frames == 0:
            raise ValueError(
                "Cannot evaluate an empty frame sequence"
            )

        # --------------------------------------------------
        # Calculate unusable frames
        # --------------------------------------------------
        unusable_frames = (
            total_frames - usable_frames
        )

        # --------------------------------------------------
        # Calculate usable percentage
        # --------------------------------------------------

        usable_percentage = (
            usable_frames / total_frames
        ) * 100.0

        # --------------------------------------------------
        # Calculate ANPR capture window
        # --------------------------------------------------
        if first_usable_frame is not None:

            first_usable_time_s = (
                    first_usable_frame / self.fps
            )

            last_usable_time_s = (
                    last_usable_frame / self.fps
            )

            capture_window_s = (
                    (
                            last_usable_frame
                            - first_usable_frame
                            + 1
                    )
                    / self.fps
            )

        else:

            first_usable_time_s = None
            last_usable_time_s = None
            capture_window_s = 0.0

        return ANPREvaluation(
            total_frames=total_frames,
            usable_frames=usable_frames,
            unusable_frames=unusable_frames,
            usable_percentage=usable_percentage,
            first_usable_frame=first_usable_frame,
            last_usable_frame=last_usable_frame,
            first_usable_time_s=first_usable_time_s,
            last_usable_time_s=last_usable_time_s,
            capture_window_s=capture_window_s,
            maximum_plate_width_pixels=(
                maximum_plate_width_pixels
            ),
            maximum_plate_height_pixels=(
                maximum_plate_height_pixels
            ),
        )