import yaml
from .camera import (
    CameraConfig,
    Resolution,
    ActiveAreaConfig,
    ActivePixelConfig,
    SensorConfig,
    LensConfig,
    FOVRangeConfig,
    FOVConfig,
    FPSConfig,
    ShutterConfig
)

def load_camera_config(file_path: str) -> dict:
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)

    except yaml.YAMLError:
        raise ValueError("Camera Config must be a valid yaml file")

    if config is None:
        return {}
    if not isinstance(config, dict):
        raise ValueError("Camera Config must be a dict")

    return config

def create_camera_config(config: dict) -> CameraConfig:
    resolution = Resolution(
        width=config["sensor"]["resolution"]["width"],
        height=config["sensor"]["resolution"]["height"]
    )

    active_area = ActiveAreaConfig(
        width = config["sensor"]["active_area"]["width"],
        height = config["sensor"]["active_area"]["height"]
    )
    active_pixel = ActivePixelConfig(
        width = config["sensor"]["active_pixel"]["width"],
        height = config["sensor"]["active_pixel"]["height"]
    )
    sensor_config = SensorConfig(
        format = config["sensor"]["format"],
        name = config["sensor"]["name"],
        pixel_size = config["sensor"]["pixel_size"],
        resolution = resolution,
        active_area = active_area,
        active_pixel = active_pixel
    )
    lens_config = LensConfig(
        type = config["lens"]["type"],
        min_focal_length_mm = config["lens"]["min_focal_length_mm"],
        max_focal_length_mm = config["lens"]["max_focal_length_mm"]
    )
    wide = FOVConfig(
        focal_length_mm = config["fov"]["wide"]["focal_length_mm"],
        horizontal_fov_deg = config["fov"]["wide"]["horizontal_deg"],
        vertical_fov_deg = config["fov"]["wide"]["vertical_deg"]
    )
    tele = FOVConfig(
        focal_length_mm = config["fov"]["tele"]["focal_length_mm"],
        horizontal_fov_deg = config["fov"]["tele"]["horizontal_deg"],
        vertical_fov_deg = config["fov"]["tele"]["vertical_deg"]
    )
    fov_range_config = FOVRangeConfig(
        wide = wide,
        tele = tele
    )
    fps_config = FPSConfig(
        min = config["fps"]["min"],
        max = config["fps"]["max"]
    )
    shutter_config = ShutterConfig(
        min_speed=config["shutter"]["min_seconds"],
        max_speed=config["shutter"]["max_seconds"],
    )

    return CameraConfig(
        name = config["name"],
        sensor_config = sensor_config,
        lens_config = lens_config,
        fov_range_config = fov_range_config,
        fps_config = fps_config,
        shutter_config = shutter_config
    )

def load_camera(file_path: str) -> CameraConfig:
    try:
        config = load_camera_config(file_path)
        return create_camera_config(config)


    except FileNotFoundError as error:
        raise FileNotFoundError(
            f"Camera config file not found: {file_path}"
        ) from error
    except ValueError as error:
        raise ValueError(
            f"Camera config file invalid: {file_path}"
        ) from error

