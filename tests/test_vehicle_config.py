import pytest
from pathlib import Path
from anpr_simulator.vehicle.config_loader import load_vehicle
from anpr_simulator.vehicle.config_validator import validate_vehicle_config


def get_vehicle_config_file():
    return (
        Path(__file__).parent.parent
        / "config"
        / "vehicle"
        / "vehicle_config.yaml"
    )


def test_load_vehicle_success():

    vehicle = load_vehicle(
        str(get_vehicle_config_file())
    )
    if vehicle is None:
        pytest.fail("failed to load vehicle configuration")

    validate_vehicle_config(vehicle)