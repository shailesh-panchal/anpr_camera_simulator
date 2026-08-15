from .camera import FOVConfig, CameraConfig, Resolution, ActiveAreaConfig, ActivePixelConfig


def validate_resolution(resolution: Resolution) -> None:
    if resolution.width <= 0:
        raise ValueError("Camera resolution width must be greater than 0")

    if resolution.height <= 0:
        raise ValueError("Camera resolution height must be greater than 0")

def validate_active_area(active_area: ActiveAreaConfig) -> None:
    if active_area.width <= 0:
        raise ValueError("Camera active_area width must be greater than 0")
    if active_area.height <= 0:
        raise ValueError("Camera active_area height must be greater than 0")

def validate_pixel_size(pixel_size: float) -> None:
    if pixel_size <= 0:
        raise ValueError("Camera pixel_size must be greater than 0")

def validate_active_pixel(active_pixel: ActivePixelConfig) -> None:
    if active_pixel.width <= 0:
        raise ValueError("Camera active_pixel width must be greater than 0")
    if active_pixel.height <= 0:
        raise ValueError("Camera active_pixel height must be greater than 0")

def validate_lens_config(min_focal_length_mm: float, max_focal_lengt_mm : float) -> None:
    if min_focal_length_mm <= 0:
        raise ValueError("Camera lens min_focal_length_mm must be greater than 0")
    if max_focal_lengt_mm <= 0:
        raise ValueError("Camera lens max_focal_lengt_mm must be greater than 0")
    if min_focal_length_mm > max_focal_lengt_mm:
        raise ValueError("Camera lens min_focal_length_mm must be less than max_focal_lengt_mm")


def validate_fov_range_config(wide : FOVConfig, tele : FOVConfig) -> None:
    if wide.horizontal_fov_deg <= 0:
        raise ValueError("Camera lens horizontal_fov_mm must be greater than 0")
    if wide.vertical_fov_deg <= 0:
        raise ValueError("Camera lens vertical_fov_mm must be greater than 0")
    if wide.focal_length_mm <= 0:
        raise ValueError("Camera lens focal_length_mm must be greater than 0")
    if tele.horizontal_fov_deg <= 0:
        raise ValueError("Camera lens horizontal_fov_mm must be greater than 0")
    if tele.vertical_fov_deg <= 0:
        raise ValueError("Camera lens vertical_fov_mm must be greater than 0")
    if tele.focal_length_mm <= 0:
        raise ValueError("Camera lens focal_length_mm must be greater than 0")
    if wide.focal_length_mm >= tele.focal_length_mm:
        raise ValueError("Camera lens wide focal_length_mm must be less than tele.focal_length_mm")

def validate_fps(min : int, max : int) -> None:
    if min <= 0:
        raise ValueError("Camera fps must be greater than 0")
    if max <= 0:
        raise ValueError("Camera fps must be greater than 0")
    if min > max:
        raise ValueError("Camera fps must be less than max")

def validate_shutter_speed(min : int, max : int) -> None:
    if min <= 0:
        raise ValueError("Camera shutter speed must be greater than 0")
    if max <= 0:
        raise ValueError("Camera shutter speed must be greater than 0")
    if min > max:
        raise ValueError("Camera shutter speed must be less than max")

def validate_camera_config(config: CameraConfig) -> None:
    validate_resolution(config.sensor_config.resolution)
    validate_active_area(config.sensor_config.active_area)
    validate_pixel_size(config.sensor_config.pixel_size)
    validate_active_pixel(config.sensor_config.active_pixel)
    validate_lens_config(config.lens_config.min_focal_length_mm, config.lens_config.max_focal_length_mm)
    validate_fov_range_config(config.fov_range_config.wide, config.fov_range_config.tele)
    validate_fps(config.fps_config.min, config.fps_config.max)
    validate_shutter_speed(config.shutter_config.min_speed, config.shutter_config.max_speed)
