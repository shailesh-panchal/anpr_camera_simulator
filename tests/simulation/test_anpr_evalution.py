from anpr_simulator.simulation.anpr_evaluation import (
    ANPREvaluation,
)


def test_anpr_evaluation():

    evaluation = ANPREvaluation(
        total_frames=300,
        usable_frames=60,
        unusable_frames=240,
        usable_percentage=20.0,
        first_usable_frame=85,
        last_usable_frame=144,
        maximum_plate_width_pixels=180.0,
        maximum_plate_height_pixels=38.0,
    )

    assert evaluation.total_frames == 300
    assert evaluation.usable_frames == 60
    assert evaluation.unusable_frames == 240

    assert evaluation.usable_percentage == 20.0

    assert evaluation.first_usable_frame == 85
    assert evaluation.last_usable_frame == 144

    assert (
        evaluation.maximum_plate_width_pixels
        == 180.0
    )

    assert (
        evaluation.maximum_plate_height_pixels
        == 38.0
    )


def test_no_usable_frames():

    evaluation = ANPREvaluation(
        total_frames=300,
        usable_frames=0,
        unusable_frames=300,
        usable_percentage=0.0,
        first_usable_frame=None,
        last_usable_frame=None,
        maximum_plate_width_pixels=80.0,
        maximum_plate_height_pixels=15.0,
    )

    assert evaluation.usable_frames == 0
    assert evaluation.first_usable_frame is None
    assert evaluation.last_usable_frame is None