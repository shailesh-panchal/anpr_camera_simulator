from dataclasses import dataclass

from anpr_simulator.geometry.camera_intrinsics import CameraIntrinsics
from anpr_simulator.geometry.camera_pose import CameraPose
from anpr_simulator.geometry.license_plate import LicensePlateDimensions
from anpr_simulator.geometry.vehicle import VehicleDimensions
from anpr_simulator.geometry.vehicle_trajectory import VehicleTrajectory


@dataclass(frozen=True)
class SimulationScenario:
    """
    Complete configuration for one ANPR simulation scenario.
    """

    name: str

    fps: float
    duration_s: float

    camera_pose: CameraPose
    intrinsics: CameraIntrinsics

    vehicle_dimensions: VehicleDimensions
    plate_dimensions: LicensePlateDimensions

    trajectory: VehicleTrajectory

    def __post_init__(self) -> None:

        if not self.name:
            raise ValueError(
                "Scenario name cannot be empty"
            )

        if self.fps <= 0:
            raise ValueError(
                "FPS must be greater than zero"
            )

        if self.duration_s <= 0:
            raise ValueError(
                "Duration must be greater than zero"
            )

