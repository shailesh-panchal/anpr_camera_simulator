from collections.abc import Iterator

from iniconfig import exceptions

from anpr_simulator.geometry.camera_intrinsics import (
    CameraIntrinsics,
)
from anpr_simulator.geometry.camera_pose import (
    CameraPose,
)
from anpr_simulator.geometry.license_plate import (
    LicensePlateDimensions,
)
from anpr_simulator.geometry.vehicle import (
    VehicleDimensions,
)
from anpr_simulator.geometry.vehicle_trajectory import (
    VehicleTrajectory,
)
from anpr_simulator.simulation.frame_simulator import (
    simulate_frame,
)
from anpr_simulator.simulation.simulation_frame import (
    SimulationFrame,
)
from anpr_simulator.simulation.scenario import (
    SimulationScenario,
)


class FrameGenerator:
    """
    Generates simulated camera frames at a fixed FPS.
    """

    def __init__(
        self,
        scenario: SimulationScenario,
    ) -> None:

        self.scenario = scenario


    def generate(self) -> Iterator[SimulationFrame]:
        """
        Generate simulation frames from t=0
        until the requested duration.
        """

        frame_interval_s = 1.0 / self.scenario.fps

        frame_number = 0
        time_s = 0.0

        while time_s < self.scenario.duration_s:
            try:
                frame = simulate_frame(
                    trajectory=self.scenario.trajectory,
                    vehicle_dimensions=self.scenario.vehicle_dimensions,
                    plate_dimensions=self.scenario.plate_dimensions,
                    camera_pose=self.scenario.camera_pose,
                    intrinsics=self.scenario.intrinsics,
                    frame_number=frame_number,
                    time_s=time_s,
                )
                yield frame

            except ValueError as error:
                print(f"Skipping frame {frame_number} at {time_s:.2f}s | ValueError: {error}")
                break

            finally:
                frame_number += 1
                time_s = frame_number * frame_interval_s

