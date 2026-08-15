from pathlib import Path

from anpr_simulator.camera.config_loader import load_camera_config


def get_load_camera_config():

    config_file = (
        Path(__file__).parent.parent
        / "config"
        / "cameras"
        / "satatya_cibr20mvl12cwp_p2.yaml"
    )

    return config_file

def test_camera_name():
    config = load_camera_config(
        str(get_load_camera_config())
    )

    assert config["name"] == "SATATYA_CIBR20MVL12CWP_P2"

def test_camera_resolution():

    config = load_camera_config(
        str(get_load_camera_config())
    )

    assert config["sensor"]["resolution"]["width"] == 1920
    assert config["sensor"]["resolution"]["height"] == 1080
