
from anpr_simulator.geometry.camera_intrinsics import (
    CameraIntrinsics,
)
from anpr_simulator.geometry.camera_pose import (
    CameraPose,
)
from anpr_simulator.geometry.license_plate import (
    LicensePlateDimensions,
)
from anpr_simulator.geometry.plate_projection import (
    project_vehicle_plate,
)
from anpr_simulator.geometry.vehicle import (
    VehicleDimensions,
)
from anpr_simulator.geometry.vehicle_state import (
    vehicle_state_at_time,
)
from anpr_simulator.geometry.vehicle_trajectory import (
    VehicleTrajectory,
)

from anpr_simulator.simulation.simulation_frame import (
    SimulationFrame,
)

def simulate_frame(
    trajectory: VehicleTrajectory,
    vehicle_dimensions: VehicleDimensions,
    plate_dimensions: LicensePlateDimensions,
    camera_pose: CameraPose,
    intrinsics: CameraIntrinsics,
    frame_number: int,
    time_s: float,
) -> SimulationFrame:

    vehicle_state = vehicle_state_at_time(
        trajectory,
        vehicle_dimensions,
        time_s,
    )

    projected_plate = project_vehicle_plate(
        vehicle_state=vehicle_state,
        plate_dimensions=plate_dimensions,
        camera_pose=camera_pose,
        intrinsics=intrinsics,
    )

    return SimulationFrame(
        frame_number=frame_number,
        timestamp_s=time_s,
        vehicle_state=vehicle_state,
        projected_plate=projected_plate,
    )