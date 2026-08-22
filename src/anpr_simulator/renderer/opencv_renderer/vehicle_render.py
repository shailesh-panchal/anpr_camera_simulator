import numpy as np
import cv2

from anpr_simulator.renderer.opencv_renderer.renderer import (
    Resolution,
    create_frame,
    add_background
)
import cv2
import numpy as np


def render_vehicle(
        frame: np.ndarray,
        vehicle_position: tuple[int, int],
        vehicle_size: tuple[int, int],
        vehicle_color: tuple[int, int, int],
) -> np.ndarray:
    """
    Renders a solid rectangle representing a vehicle with strict parameter validation.

    Parameters:
    - frame: The input background image array.
    - vehicle_position: A tuple (x, y) specifying the top-left corner.
    - vehicle_size: A tuple (width, height) specifying vehicle dimensions.
    - vehicle_color: A tuple (B, G, R) specifying the fill color.

    Returns:
    - The frame with the vehicle rendered on it (or untouched if validation fails).
    """
    # 1. Validate frame structure
    if frame is None or not isinstance(frame, np.ndarray) or len(frame.shape) != 3:
        raise ValueError("Invalid frame: Must be a valid 3-channel numpy array.")

    frame_height, frame_width, _ = frame.shape
    x, y = vehicle_position
    width, height = vehicle_size

    # 2. Validate vehicle dimensions
    if width <= 0 or height <= 0:
        raise ValueError(f"Invalid size {vehicle_size}: Width and height must be greater than 0.")

    # 3. Validate vehicle color channels (BGR must be 0-255)
    if not all(0 <= channel <= 255 for channel in vehicle_color):
        raise ValueError(f"Invalid color {vehicle_color}: BGR values must be between 0 and 255.")

    # 4. Check boundaries (Vehicle must at least partially intersect the frame)
    bottom_right_x = x + width
    bottom_right_y = y + height

    if bottom_right_x <= 0 or x >= frame_width or bottom_right_y <= 0 or y >= frame_height:
        print(f"Warning: Vehicle at {vehicle_position} with size {vehicle_size} is completely off-screen.")
        return frame  # Return early without drawing to prevent errors

    # 5. Clip coordinates to frame boundaries to ensure safe drawing
    safe_top_left = (max(0, x), max(0, y))
    safe_bottom_right = (min(frame_width, bottom_right_x), min(frame_height, bottom_right_y))

    # Draw the vehicle rectangle (thickness=-1 fills the shape entirely)
    cv2.rectangle(frame, safe_top_left, safe_bottom_right, vehicle_color, thickness=-1)

    return frame
