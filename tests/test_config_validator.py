import pytest
from pathlib import Path
from anpr_simulator.camera.config_loader import load_camera
from anpr_simulator.camera.config_validator import validate_camera_config


def get_camera_config_file():
    return (
        Path(__file__).parent.parent
        / "config"
        / "cameras"
        / "satatya_cibr20mvl12cwp_p2.yaml"
    )


def test_load_camera_success():

    camera = load_camera(
        str(get_camera_config_file())
    )
    if camera is None:
        pytest.fail("Camera not loaded")

    validate_camera_config(camera)