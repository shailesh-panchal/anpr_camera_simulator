import cv2
import numpy as np


def render_license_plate(
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
