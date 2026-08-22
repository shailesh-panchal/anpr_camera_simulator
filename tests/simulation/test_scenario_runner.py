from anpr_simulator.simulation.anpr_scenario import create_150_kmh_scenario
from anpr_simulator.simulation.frame_generator import FrameGenerator
from anpr_simulator.simulation.scenario_runner import ScenarioRunner
def test_150_kmh_scenario_result():

    scenario = create_150_kmh_scenario()

    generator = FrameGenerator(
        scenario
    )

    runner = ScenarioRunner()

    result = runner.run(
        generator
    )

    assert result.scenario_name == "ANPR_150KMH"

    assert result.total_frames == 300

    assert result.first_frame_number == 0

    assert result.last_frame_number == 299

    assert result.maximum_plate_width_pixels > 0

    assert result.maximum_plate_height_pixels > 0

    assert result.minimum_plate_distance_m < (
        result.maximum_plate_distance_m
    )