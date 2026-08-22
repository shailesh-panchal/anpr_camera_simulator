import pytest

from anpr_simulator.simulation.anpr_criteria import (
    ANPRCriteria,
)


def test_valid_anpr_criteria():

    criteria = ANPRCriteria(
        minimum_plate_width_pixels=120,
        minimum_plate_height_pixels=25,
    )

    assert criteria.minimum_plate_width_pixels == 120
    assert criteria.minimum_plate_height_pixels == 25


def test_invalid_plate_width():

    with pytest.raises(ValueError):

        ANPRCriteria(
            minimum_plate_width_pixels=0,
            minimum_plate_height_pixels=25,
        )


def test_invalid_plate_height():

    with pytest.raises(ValueError):

        ANPRCriteria(
            minimum_plate_width_pixels=120,
            minimum_plate_height_pixels=0,
        )

