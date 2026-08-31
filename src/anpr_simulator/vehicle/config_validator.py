from .vehicle import (
    VehicleConfig,
    VehicleDimConfig,
    LicencePlateConfig
)


def validate_vehicle_type(vehicle_type: str) -> None:
    allowed_types = {"two_wheeler", "three_wheeler", "four_wheeler"}

    # Strip whitespace to prevent hidden empty inputs
    cleaned_type = vehicle_type.strip()

    if not cleaned_type:
        raise ValueError("Vehicle type cannot be empty.")

    if cleaned_type not in allowed_types:
        raise ValueError(
            f"Invalid vehicle type '{vehicle_type}'. Must be one of {allowed_types}"
        )


def validate_vehicle_dim(dim : VehicleDimConfig) -> None:
    if dim.height_m <= 0:
        raise ValueError("Vehicle height must be greater than 0")
    if dim.width_m <= 0:
        raise ValueError("Vehicle width must be greater than 0")
    if dim.length_m <= 0:
        raise ValueError("Vehicle length must be greater than 0")


def validate_number_plate_dim(dim : LicencePlateConfig) -> None:
    if dim.width_m <= 0:
        raise ValueError("Licence plate width must be greater than 0")
    if dim.height_m <= 0:
        raise ValueError("Licence plate height must be greater than 0")
    if dim.mounted_height_m <= 0:
        raise ValueError("Licence plate height must be greater than 0")


def validate_vehicle_config(config: VehicleConfig) -> None:
    validate_vehicle_dim(config.dim)
    validate_number_plate_dim(config.front_plate_config)
    validate_number_plate_dim(config.back_plate_config)
    validate_vehicle_type(config.type)