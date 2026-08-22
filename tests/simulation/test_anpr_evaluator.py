from types import SimpleNamespace

from anpr_simulator.simulation.anpr_criteria import (
    ANPRCriteria,
)
from anpr_simulator.simulation.anpr_evaluator import (
    ANPREvaluator,
)
from anpr_simulator.simulation.anpr_scenario import (
    create_150_kmh_scenario,
)

from anpr_simulator.simulation.frame_generator import (
    FrameGenerator,
)

def test_150_kmh_anpr_evaluation():

    scenario = create_150_kmh_scenario()

    generator = FrameGenerator(
        scenario
    )

    criteria = ANPRCriteria(
        minimum_plate_width_pixels=120,
        minimum_plate_height_pixels=25,
    )
    fps = 60
    evaluator = ANPREvaluator(
        criteria,
        fps
    )

    result = evaluator.evaluate(
        generator.generate()
    )

    assert result.total_frames == 300

    assert result.usable_frames >= 0

    assert result.usable_frames <= (
        result.total_frames
    )

    assert result.unusable_frames == (
        result.total_frames
        - result.usable_frames
    )

    assert 0.0 <= (
        result.usable_percentage
    ) <= 100.0


def create_test_frame(
    frame_number: int,
    plate_width: float,
    plate_height: float,
):
    """
    Create a minimal SimulationFrame-like object
    for testing ANPREvaluator.

    We only need projected_plate.width_pixels
    and projected_plate.height_pixels.
    """

    plate = SimpleNamespace(
        width_pixels=plate_width,
        height_pixels=plate_height,
    )

    return SimpleNamespace(
        frame_number=frame_number,
        projected_plate=plate,
    )


def test_anpr_evaluator_acceptance_criteria():

    frames = [
        create_test_frame(
            frame_number=0,
            plate_width=80,
            plate_height=15,
        ),
        create_test_frame(
            frame_number=1,
            plate_width=100,
            plate_height=20,
        ),
        create_test_frame(
            frame_number=2,
            plate_width=120,
            plate_height=25,
        ),
        create_test_frame(
            frame_number=3,
            plate_width=150,
            plate_height=30,
        ),
        create_test_frame(
            frame_number=4,
            plate_width=200,
            plate_height=40,
        ),
    ]

    criteria = ANPRCriteria(
        minimum_plate_width_pixels=120,
        minimum_plate_height_pixels=25,
    )
    fps = 60
    evaluator = ANPREvaluator(
        criteria,
        fps
    )

    result = evaluator.evaluate(
        frames
    )

    assert result.total_frames == 5

    assert result.usable_frames == 3

    assert result.unusable_frames == 2

    assert result.usable_percentage == 60.0

    assert result.first_usable_frame == 2

    assert result.last_usable_frame == 4

    assert (
        result.maximum_plate_width_pixels
        == 200
    )

    assert (
        result.maximum_plate_height_pixels
        == 40
    )

def test_anpr_evaluator_accepts_generator():

    def frame_generator():

        yield create_test_frame(
            frame_number=0,
            plate_width=80,
            plate_height=15,
        )

        yield create_test_frame(
            frame_number=1,
            plate_width=150,
            plate_height=30,
        )

    criteria = ANPRCriteria(
        minimum_plate_width_pixels=120,
        minimum_plate_height_pixels=25,
    )
    fps = 60
    evaluator = ANPREvaluator(
        criteria,
        fps
    )

    result = evaluator.evaluate(
        frame_generator()
    )

    assert result.total_frames == 2

    assert result.usable_frames == 1

    assert result.unusable_frames == 1

    assert result.first_usable_frame == 1

    assert result.last_usable_frame == 1

    assert result.usable_percentage == 50.0