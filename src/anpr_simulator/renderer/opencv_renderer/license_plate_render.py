import cv2
import numpy as np

from anpr_simulator.geometry.plate_projection import ProjectedPlate

def create_license_plate(
        plate_number: str,
        plate_size: tuple[int, int],
        background_color: tuple[int, int, int],
        text_color: tuple[int, int, int],
) -> np.ndarray:
    """
    Generates a synthetic license plate image with centered text.

    Parameters:
    - plate_number: The alphanumeric text string to display on the plate.
    - plate_size: A tuple (width, height) specifying plate dimensions in pixels.
    - background_color: A tuple (B, G, R) for the plate background.
    - text_color: A tuple (B, G, R) for the text characters.

    Returns:
    - A standalone NumPy ndarray image containing the generated license plate.
    """
    # 1. Validation
    width, height = plate_size
    if width <= 0 or height <= 0:
        raise ValueError(f"Invalid plate size {plate_size}: Dimensions must be greater than 0.")
    if not plate_number.strip():
        raise ValueError("Plate number string cannot be empty.")
    if not all(0 <= c <= 255 for c in background_color + text_color):
        raise ValueError("Color channel values must be between 0 and 255.")

    # 2. Create base canvas for the plate
    plate_img = np.full((height, width, 3), background_color, dtype=np.uint8)

    # 3. Choose font asset
    font = cv2.FONT_HERSHEY_SIMPLEX
    thickness = max(1, int(height * 0.05))  # Scales line width proportionally to height

    # 4. Dynamically compute the best font scale to fit inside dimensions safely
    # Start with a reference scale and check text size metrics
    target_text_width = int(width * 0.85)  # Leave a small margin horizontally
    text_size, _ = cv2.getTextSize(plate_number, font, fontScale=1.0, thickness=thickness)

    # Calculate scale factor relative to our target width bounding box
    font_scale = target_text_width / text_size[0]

    # Re-calculate with final scale to secure precise final bounding coordinates
    final_text_size, baseline = cv2.getTextSize(plate_number, font, fontScale=font_scale, thickness=thickness)

    # 5. Center text alignment mathematical calculation
    text_x = (width - final_text_size[0]) // 2
    text_y = (height + final_text_size[1]) // 2  # Flips vertical offset baseline

    # 6. Draw characters on the target matrix
    cv2.putText(
        plate_img,
        plate_number,
        (text_x, text_y),
        font,
        font_scale,
        text_color,
        thickness,
        lineType=cv2.LINE_AA
    )

    return plate_img


def render_license_plate(
        frame: np.ndarray,
        plate: np.ndarray,
        position: tuple[int, int],
) -> np.ndarray:
    """
    Overlays a license plate image onto a parent video frame at the specified coordinate.
     Handles cropping gracefully if the plate is partially or fully off-screen.

    Parameters:
    - frame: The main background scene or vehicle image array.
    - plate: The standalone license plate image array generated in M3.
    - position: A tuple (x, y) specifying the top-left placement coordinates on the frame.

    Returns:
    - The composite frame with the license plate overlaid.
    """
    # 1. Structural Validations
    if frame is None or plate is None:
        raise ValueError("Input arrays cannot be None.")
    if len(frame.shape) != 3 or len(plate.shape) != 3:
        raise ValueError("Both frame and plate must be 3-channel image arrays.")

    frame_h, frame_width, _ = frame.shape
    plate_h, plate_w, _ = plate.shape
    x, y = position

    # 2. Early return check if completely out of bounds
    if x >= frame_width or y >= frame_h or (x + plate_w) <= 0 or (y + plate_h) <= 0:
        return frame

    # 3. Calculate overlapping intersection boundaries (Slicing ranges)
    # Target coordinates on the main frame
    f_x1 = max(0, x)
    f_y1 = max(0, y)
    f_x2 = min(frame_width, x + plate_w)
    f_y2 = min(frame_h, y + plate_h)

    # Source coordinates on the local license plate matrix
    p_x1 = max(0, -x)
    p_y1 = max(0, -y)
    p_x2 = p_x1 + (f_x2 - f_x1)
    p_y2 = p_y1 + (f_y2 - f_y1)

    # 4. Overwrite frame region with the plate slice
    frame[f_y1:f_y2, f_x1:f_x2] = plate[p_y1:p_y2, p_x1:p_x2]

    return frame


def render_projected_license_plate(
    frame: np.ndarray,
    plate: np.ndarray,
    projected_plate: ProjectedPlate,
) -> np.ndarray:
    """
    Render a license plate onto a frame using the projected
    four corner coordinates.

    Parameters:
    - frame:
        Destination camera frame. Expected shape:
        (height, width, 3).

    - plate:
        Source license plate image. Expected shape:
        (height, width, 3).

    - projected_plate:
        Projected license plate geometry containing:
        top_left
        top_right
        bottom_left
        bottom_right

    Returns:
    - Frame with the projected license plate composited onto it.
    """

    # ---------------------------------------------------------
    # 1. Validate input
    # ---------------------------------------------------------

    if frame is None or plate is None:
        raise ValueError("Frame and plate cannot be None.")

    if projected_plate is None:
        raise ValueError("Projected plate cannot be None.")

    if not isinstance(frame, np.ndarray):
        raise TypeError("Frame must be a numpy ndarray.")

    if not isinstance(plate, np.ndarray):
        raise TypeError("Plate must be a numpy ndarray.")

    if frame.ndim != 3 or frame.shape[2] != 3:
        raise ValueError(
            "Frame must be a 3-channel image."
        )

    if plate.ndim != 3 or plate.shape[2] != 3:
        raise ValueError(
            "Plate must be a 3-channel image."
        )

    # ---------------------------------------------------------
    # 2. Get frame and plate dimensions
    # ---------------------------------------------------------

    frame_height, frame_width = frame.shape[:2]

    plate_height, plate_width = plate.shape[:2]

    # ---------------------------------------------------------
    # 3. Source points
    #
    # Original license plate image:
    #
    # (0,0) ---------------- (width-1,0)
    #   |                         |
    #   |         PLATE           |
    #   |                         |
    # (0,height-1) ------ (width-1,height-1)
    # ---------------------------------------------------------

    source_points = np.float32([
        [0, 0],
        [plate_width - 1, 0],
        [plate_width - 1, plate_height - 1],
        [0, plate_height - 1],
    ])

    # ---------------------------------------------------------
    # 4. Destination points
    #
    # OpenCV order:
    #
    # top-left
    # top-right
    # bottom-right
    # bottom-left
    # ---------------------------------------------------------

    destination_points = np.float32([
        [
            projected_plate.top_left.x,
            projected_plate.top_left.y,
        ],
        [
            projected_plate.top_right.x,
            projected_plate.top_right.y,
        ],
        [
            projected_plate.bottom_right.x,
            projected_plate.bottom_right.y,
        ],
        [
            projected_plate.bottom_left.x,
            projected_plate.bottom_left.y,
        ],
    ])

    # ---------------------------------------------------------
    # 5. Calculate perspective transformation
    # ---------------------------------------------------------

    transform_matrix = cv2.getPerspectiveTransform(
        source_points,
        destination_points,
    )

    # ---------------------------------------------------------
    # 6. Warp plate into camera-frame coordinates
    # ---------------------------------------------------------

    warped_plate = cv2.warpPerspective(
        plate,
        transform_matrix,
        (frame_width, frame_height),
    )

    # ---------------------------------------------------------
    # 7. Create mask for projected plate
    # ---------------------------------------------------------

    mask = np.zeros(
        (frame_height, frame_width),
        dtype=np.uint8,
    )

    cv2.fillConvexPoly(
        mask,
        np.int32(destination_points),
        255,
    )

    # ---------------------------------------------------------
    # 8. Composite warped plate onto frame
    # ---------------------------------------------------------

    cv2.copyTo(warped_plate, mask, frame)

    return frame