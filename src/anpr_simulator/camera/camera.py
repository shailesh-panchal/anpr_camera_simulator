
from dataclasses import dataclass

@dataclass
class ActivePixelConfig:
    width : float
    height : float

@dataclass
class ActiveAreaConfig:
    width : float
    height : float

@dataclass

@dataclass
class Resolution:
    width: int
    height: int

@dataclass
class SensorConfig:
    resolution: Resolution
    format : str
    name : str
    pixel_size : float
    active_area: ActiveAreaConfig
    active_pixel: ActivePixelConfig


@dataclass
class LensConfig:
    type : str
    min_focal_length_mm  : float
    max_focal_length_mm  : float

@dataclass
class FOVConfig:
    focal_length_mm : float
    horizontal_fov_deg : float
    vertical_fov_deg : float

@dataclass
class FOVRangeConfig:
    wide : FOVConfig
    tele : FOVConfig

@dataclass
class FPSConfig:
    min : int
    max : int

@dataclass
class ShutterConfig:
    min_speed : float
    max_speed : float

@dataclass
class CameraConfig:
    name: str
    sensor_config: SensorConfig
    lens_config: LensConfig
    fov_range_config: FOVRangeConfig
    shutter_config: ShutterConfig
    fps_config: FPSConfig
