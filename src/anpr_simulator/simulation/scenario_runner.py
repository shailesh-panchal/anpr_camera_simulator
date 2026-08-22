from anpr_simulator.simulation.frame_generator import (
    FrameGenerator,
)
from anpr_simulator.simulation.simulation_result import (
    SimulationResult,
)


class ScenarioRunner:
    """
    Executes a simulation scenario and collects
    performance measurements.
    """

    def run(
        self,
        generator: FrameGenerator,
    ) -> SimulationResult:

        total_frames = 0

        first_frame_number = None
        last_frame_number = None

        maximum_plate_width_pixels = float("-inf")
        minimum_plate_width_pixels = float("inf")

        maximum_plate_height_pixels = float("-inf")
        minimum_plate_height_pixels = float("inf")

        maximum_plate_distance_m = float("-inf")
        minimum_plate_distance_m = float("inf")

        # Process one frame at a time.
        for frame in generator.generate():

            total_frames += 1

            if first_frame_number is None:
                first_frame_number = (
                    frame.frame_number
                )

            last_frame_number = (
                frame.frame_number
            )

            plate = frame.projected_plate

            # Plate width
            maximum_plate_width_pixels = max(
                maximum_plate_width_pixels,
                plate.width_pixels,
            )

            minimum_plate_width_pixels = min(
                minimum_plate_width_pixels,
                plate.width_pixels,
            )

            # Plate height
            maximum_plate_height_pixels = max(
                maximum_plate_height_pixels,
                plate.height_pixels,
            )

            minimum_plate_height_pixels = min(
                minimum_plate_height_pixels,
                plate.height_pixels,
            )

            # Vehicle / plate distance
            distance_m = frame.vehicle_state.z_m

            maximum_plate_distance_m = max(
                maximum_plate_distance_m,
                distance_m,
            )

            minimum_plate_distance_m = min(
                minimum_plate_distance_m,
                distance_m,
            )

        if total_frames == 0:
            raise ValueError(
                "Simulation generated no frames"
            )

        return SimulationResult(
            scenario_name=generator.scenario.name,

            total_frames=total_frames,

            first_frame_number=first_frame_number,
            last_frame_number=last_frame_number,

            maximum_plate_width_pixels=(
                maximum_plate_width_pixels
            ),

            minimum_plate_width_pixels=(
                minimum_plate_width_pixels
            ),

            maximum_plate_height_pixels=(
                maximum_plate_height_pixels
            ),

            minimum_plate_height_pixels=(
                minimum_plate_height_pixels
            ),

            maximum_plate_distance_m=(
                maximum_plate_distance_m
            ),

            minimum_plate_distance_m=(
                minimum_plate_distance_m
            ),
        )