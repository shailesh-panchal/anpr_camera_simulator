from anpr_simulator.simulation.anpr_scenario import create_150_kmh_scenario
from anpr_simulator.simulation.frame_generator import FrameGenerator

def test_150_kmh_scenario():

    scenario = create_150_kmh_scenario()

    generator = FrameGenerator(
        scenario
    )

    frames = list(
        generator.generate()
    )

    assert len(frames) == 300