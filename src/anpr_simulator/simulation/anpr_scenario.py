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
    VehicleDirection
)
from anpr_simulator.simulation.scenario import (
    SimulationScenario,
)
def create_150_kmh_scenario() -> SimulationScenario:

    intrinsics = CameraIntrinsics(
        fx=973.4,
        fy=983.4,
        cx=968.0,
        cy=550.0,
    )

    camera_pose = CameraPose(
        x_m=0.0,
        y_m=5.0,
        z_m=0.0,
        pitch_deg=10.0,
    )

    vehicle = VehicleDimensions(
        length_m=4.5,
        width_m=1.8,
        height_m=1.5,
        license_plate_height_m=0.5,
    )

    plate = LicensePlateDimensions(
        width_m=0.52,
        height_m=0.11,
    )

    trajectory = VehicleTrajectory(
        initial_z_m=100.0,
        speed_mps=10.0,
        x_m=0.0,
        y_m=0.0,
        direction=VehicleDirection.APPROACHING_CAMERA,
    )

    return SimulationScenario(
        name="ANPR_150KMH",
        fps=60.0,
        duration_s=5.0,
        camera_pose=camera_pose,
        intrinsics=intrinsics,
        vehicle_dimensions=vehicle,
        plate_dimensions=plate,
        trajectory=trajectory,
    )