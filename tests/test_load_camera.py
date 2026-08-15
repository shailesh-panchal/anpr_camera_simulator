from pathlib import Path

from anpr_simulator.camera.config_loader import load_camera


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

    assert camera is not None
    assert camera.name == "SATATYA_CIBR20MVL12CWP_P2"
    assert camera.fov_range_config.tele.focal_length_mm == 12.0