from collections.abc import Iterator

import numpy as np

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
from anpr_simulator.renderer.opencv_renderer.license_plate_render import (
    create_license_plate,
    render_projected_license_plate,
)
from anpr_simulator.renderer.opencv_renderer.renderer import (
    Resolution,
    add_background,
    add_road_background,
    create_frame,
)
from anpr_simulator.renderer.opencv_renderer.vehicle_render import (
    render_vehicle,
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
        scenario: SimulationScenario | None = None,
        *,
        name: str | None = None,
        fps: float | None = None,
        duration_s: float | None = None,
        trajectory: VehicleTrajectory | None = None,
        vehicle_dimensions: VehicleDimensions | None = None,
        plate_dimensions: LicensePlateDimensions | None = None,
        camera_pose: CameraPose | None = None,
        intrinsics: CameraIntrinsics | None = None,
    ) -> None:

        if scenario is not None:
            self.scenario = scenario
            return

        if fps is None or duration_s is None:
            raise ValueError("fps and duration_s are required when scenario is not provided.")

        if trajectory is None or vehicle_dimensions is None or plate_dimensions is None:
            raise ValueError(
                "trajectory, vehicle_dimensions, and plate_dimensions are required when scenario is not provided."
            )

        if camera_pose is None or intrinsics is None:
            raise ValueError("camera_pose and intrinsics are required when scenario is not provided.")

        self.scenario = SimulationScenario(
            name=name or "generated_scenario",
            fps=fps,
            duration_s=duration_s,
            camera_pose=camera_pose,
            intrinsics=intrinsics,
            vehicle_dimensions=vehicle_dimensions,
            plate_dimensions=plate_dimensions,
            trajectory=trajectory,
        )

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

    def render_frame(
        self,
        frame_data: SimulationFrame,
        *,
        plate_number: str = "KA01AB1234",
        frame_size: tuple[int, int] = (1920, 1080),
        vehicle_size: tuple[int, int] = (300, 120),
        vehicle_position: tuple[int, int] | None = None,
        background_color: tuple[int, int, int] = (30, 30, 30),
        vehicle_color: tuple[int, int, int] = (80, 80, 80),
        plate_background_color: tuple[int, int, int] = (255, 255, 255),
        plate_text_color: tuple[int, int, int] = (0, 0, 0),
        include_background: bool = True,
        include_vehicle: bool = True,
    ) -> np.ndarray:
        """
        Composite a real OpenCV scene from a simulated geometry frame.
        """

        width, height = frame_size
        rendered = create_frame(Resolution(width=width, height=height), 3)

        if include_background:
            rendered = add_road_background(
                rendered,
                sky_color=background_color,
                road_color=(55, 55, 55),
                lane_color=(220, 220, 220),
                horizon_y_ratio=0.62,
            )
        else:
            rendered[:] = background_color

        if include_vehicle:
            if vehicle_position is None:
                vehicle_position = (max(0, int(width * 0.10)), max(0, int(height * 0.60)))

            rendered = render_vehicle(
                frame=rendered,
                vehicle_position=vehicle_position,
                vehicle_size=vehicle_size,
                vehicle_color=vehicle_color,
            )

        plate = create_license_plate(
            plate_number=plate_number,
            plate_size=(max(80, int(frame_size[0] * 0.18)), max(30, int(frame_size[1] * 0.08))),
            background_color=plate_background_color,
            text_color=plate_text_color,
        )

        rendered = render_projected_license_plate(
            frame=rendered,
            plate=plate,
            projected_plate=frame_data.projected_plate,
        )

        return rendered

    def generate_rendered(
        self,
        *,
        plate_number: str = "KA01AB1234",
        frame_size: tuple[int, int] = (1920, 1080),
        vehicle_size: tuple[int, int] = (300, 120),
        vehicle_position: tuple[int, int] | None = None,
        background_color: tuple[int, int, int] = (30, 30, 30),
        vehicle_color: tuple[int, int, int] = (80, 80, 80),
        plate_background_color: tuple[int, int, int] = (255, 255, 255),
        plate_text_color: tuple[int, int, int] = (0, 0, 0),
        include_background: bool = True,
        include_vehicle: bool = True,
    ) -> Iterator[np.ndarray]:
        """
        Yield real OpenCV frames for every simulated geometry frame.
        """

        for frame_data in self.generate():
            yield self.render_frame(
                frame_data,
                plate_number=plate_number,
                frame_size=frame_size,
                vehicle_size=vehicle_size,
                vehicle_position=vehicle_position,
                background_color=background_color,
                vehicle_color=vehicle_color,
                plate_background_color=plate_background_color,
                plate_text_color=plate_text_color,
                include_background=include_background,
                include_vehicle=include_vehicle,
            )

