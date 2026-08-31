import yaml
from .vehicle import (
    VehicleConfig,
    VehicleDimConfig,
    LicencePlateConfig
)

def load_vehicle_config(file_path: str) -> dict:
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)

    except yaml.YAMLError:
        raise ValueError("Vehicle Config must be a valid yaml file")

    if config is None:
        return {}
    if not isinstance(config, dict):
        raise ValueError("Vehicle Config must be a dict")

    return config

def create_vehicle_config(config: dict) -> VehicleConfig:
    dimension_config = VehicleDimConfig(
        width_m = config["vehicle"]["dimensions"]["width_meters"],
        height_m = config["vehicle"]["dimensions"]["height_meters"],
        length_m = config["vehicle"]["dimensions"]["length_meters"]
    )

    front_license_config = LicencePlateConfig(
        is_present = config["number_plates"]["front"]["is_present"],
        mounted_height_m= config["number_plates"]["front"]["mount_height_meters"],
        width_m= config["number_plates"]["front"]["dimensions"]["width_meters"],
        height_m= config["number_plates"]["front"]["dimensions"]["height_meters"],
    )

    back_license_config = LicencePlateConfig(
        is_present=config["number_plates"]["back"]["is_present"],
        mounted_height_m=config["number_plates"]["back"]["mount_height_meters"],
        width_m=config["number_plates"]["back"]["dimensions"]["width_meters"],
        height_m=config["number_plates"]["back"]["dimensions"]["height_meters"],
    )

    return VehicleConfig(
        type = config["vehicle"]["type"],
        dim = dimension_config,
        front_plate_config = front_license_config,
        back_plate_config = back_license_config,
    )

def load_vehicle(file_path: str) -> VehicleConfig:
    try:
        config = load_vehicle_config(file_path)
        return create_vehicle_config(config)


    except FileNotFoundError as error:
        raise FileNotFoundError(
            f"Vehicle config file not found: {file_path}"
        ) from error
    except ValueError as error:
        raise ValueError(
            f"Vehicle config file invalid: {file_path}"
        ) from error

