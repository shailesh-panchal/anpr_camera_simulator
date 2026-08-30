import cv2
import numpy as np

from anpr_simulator.geometry.camera_intrinsics import CameraIntrinsics
from anpr_simulator.geometry.camera_pose import CameraPose
from anpr_simulator.geometry.projection import Point3D, project_point
from anpr_simulator.geometry.transform import world_to_camera
from anpr_simulator.geometry.vehicle import VehicleDimensions
from anpr_simulator.geometry.vehicle_state import VehicleState
from anpr_simulator.geometry.world import WorldPoint


def render_vehicle(
        frame: np.ndarray,
        vehicle_position: tuple[int, int],
        vehicle_size: tuple[int, int],
        vehicle_color: tuple[int, int, int],
) -> np.ndarray:
    """
    Render a simple vehicle silhouette with body, roof, and windshield.
    """
    if frame is None or not isinstance(frame, np.ndarray) or len(frame.shape) != 3:
        raise ValueError("Invalid frame: Must be a valid 3-channel numpy array.")

    frame_height, frame_width, _ = frame.shape
    x, y = vehicle_position
    width, height = vehicle_size

    if width <= 0 or height <= 0:
        raise ValueError(f"Invalid size {vehicle_size}: Width and height must be greater than 0.")

    if not all(0 <= channel <= 255 for channel in vehicle_color):
        raise ValueError(f"Invalid color {vehicle_color}: BGR values must be between 0 and 255.")

    bottom_right_x = x + width
    bottom_right_y = y + height

    if bottom_right_x <= 0 or x >= frame_width or bottom_right_y <= 0 or y >= frame_height:
        return frame

    x1 = max(0, x)
    y1 = max(0, y)
    x2 = min(frame_width, bottom_right_x)
    y2 = min(frame_height, bottom_right_y)

    body_pts = np.array([
        [x1, y2],
        [x1 + int(width * 0.14), y1 + int(height * 0.25)],
        [x1 + int(width * 0.86), y1 + int(height * 0.25)],
        [x2, y2],
        [x2, y1 + int(height * 0.8)],
        [x1, y1 + int(height * 0.8)],
    ], dtype=np.int32)

    cv2.fillPoly(frame, [body_pts], vehicle_color)

    window_color = (200, 200, 200)
    window_pts = np.array([
        [x1 + int(width * 0.18), y1 + int(height * 0.28)],
        [x1 + int(width * 0.82), y1 + int(height * 0.28)],
        [x1 + int(width * 0.74), y1 + int(height * 0.66)],
        [x1 + int(width * 0.26), y1 + int(height * 0.66)],
    ], dtype=np.int32)

    cv2.fillPoly(frame, [window_pts], window_color)

    headlight_color = (80, 220, 255)
    cv2.circle(frame, (x1 + int(width * 0.18), y1 + int(height * 0.80)), max(2, width // 40), headlight_color, -1)
    cv2.circle(frame, (x2 - int(width * 0.18), y1 + int(height * 0.80)), max(2, width // 40), headlight_color, -1)

    return frame


def render_vehicle_from_state(
    frame: np.ndarray,
    *,
    vehicle_state: VehicleState,
    vehicle_dimensions: VehicleDimensions,
    camera_pose: CameraPose,
    intrinsics: CameraIntrinsics,
    vehicle_color: tuple[int, int, int] = (80, 80, 80),
    panel_image: np.ndarray | None = None,
    panel_image_path: str | None = None,
) -> np.ndarray:
    """
    Project the vehicle front panel from the same state used to compute the plate.
    If a static panel image is supplied, it is warped to the projected quad for a more realistic front-panel appearance.
    """
    half_length = vehicle_dimensions.length_m / 2.0
    half_width = vehicle_dimensions.width_m / 2.0
    total_height = vehicle_dimensions.height_m

    corners_3d = [
        WorldPoint(x_m=vehicle_state.x_m - half_width, y_m=0.0, z_m=vehicle_state.z_m - half_length),
        WorldPoint(x_m=vehicle_state.x_m + half_width, y_m=0.0, z_m=vehicle_state.z_m - half_length),
        WorldPoint(x_m=vehicle_state.x_m + half_width, y_m=0.0, z_m=vehicle_state.z_m + half_length),
        WorldPoint(x_m=vehicle_state.x_m - half_width, y_m=0.0, z_m=vehicle_state.z_m + half_length),
        WorldPoint(x_m=vehicle_state.x_m - half_width, y_m=total_height, z_m=vehicle_state.z_m - half_length),
        WorldPoint(x_m=vehicle_state.x_m + half_width, y_m=total_height, z_m=vehicle_state.z_m - half_length),
        WorldPoint(x_m=vehicle_state.x_m + half_width, y_m=total_height, z_m=vehicle_state.z_m + half_length),
        WorldPoint(x_m=vehicle_state.x_m - half_width, y_m=total_height, z_m=vehicle_state.z_m + half_length),
    ]

    projected = []
    for point in corners_3d:
        camera_point = world_to_camera(point, camera_pose)
        projected.append(project_point(camera_point, intrinsics))

    pts = np.array([[int(round(p.u)), int(round(p.v))] for p in projected], dtype=np.int32)
    front_panel = np.array([pts[2], pts[3], pts[7], pts[6]], dtype=np.int32)

    if panel_image is not None:
        panel = panel_image.copy()
    elif panel_image_path is not None:
        panel = cv2.imread(panel_image_path, cv2.IMREAD_UNCHANGED)
        if panel is None:
            raise FileNotFoundError(f"Front panel image not found: {panel_image_path}")
    else:
        if cv2.contourArea(front_panel) > 0:
            cv2.fillPoly(frame, [front_panel], vehicle_color)
            cv2.polylines(frame, [front_panel], True, (30, 30, 30), 2)
        return frame

    if panel.ndim == 2:
        panel = cv2.cvtColor(panel, cv2.COLOR_GRAY2BGR)
    elif panel.shape[2] == 4:
        panel = cv2.cvtColor(panel, cv2.COLOR_BGRA2BGR)

    target_width = max(1, int(np.linalg.norm(front_panel[1] - front_panel[0])))
    target_height = max(1, int(np.linalg.norm(front_panel[2] - front_panel[1])))

    panel_h, panel_w = panel.shape[:2]
    target_aspect = target_width / max(1, target_height)
    source_aspect = panel_w / max(1, panel_h)

    if source_aspect > target_aspect:
        scale = target_width / max(1, panel_w)
    else:
        scale = target_height / max(1, panel_h)

    resized_w = max(1, int(round(panel_w * scale)))
    resized_h = max(1, int(round(panel_h * scale)))
    panel = cv2.resize(panel, (resized_w, resized_h), interpolation=cv2.INTER_LINEAR)

    source_points = np.float32([
        [0, 0],
        [resized_w - 1, 0],
        [resized_w - 1, resized_h - 1],
        [0, resized_h - 1],
    ])
    destination_points = np.float32([front_panel[0], front_panel[1], front_panel[2], front_panel[3]])

    transform = cv2.getPerspectiveTransform(source_points, destination_points)
    warped = cv2.warpPerspective(panel, transform, (frame.shape[1], frame.shape[0]))

    mask = np.zeros((frame.shape[0], frame.shape[1]), dtype=np.uint8)
    cv2.fillConvexPoly(mask, np.int32(front_panel), 255)
    cv2.copyTo(warped, mask, frame)
    return frame
