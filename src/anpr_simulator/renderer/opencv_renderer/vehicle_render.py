import cv2
import numpy as np


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
