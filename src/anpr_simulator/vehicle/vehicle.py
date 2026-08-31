from dataclasses import dataclass

@dataclass
class VehicleDimConfig:
    height_m: float
    width_m: float
    length_m: float

@dataclass
class LicencePlateConfig:
    is_present : bool
    mounted_height_m : float
    height_m : float
    width_m : float


@dataclass
class VehicleConfig:
    type: str
    dim: VehicleDimConfig
    front_plate_config: LicencePlateConfig
    back_plate_config: LicencePlateConfig

