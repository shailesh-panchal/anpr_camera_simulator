from dataclasses import dataclass


@dataclass(frozen=True)
class Road:
    """
    Represents the road used by the simulation.

    width_m:
        Width of the road.

    length_m:
        Simulated road length.
    """

    width_m: float
    length_m: float

    def __post_init__(self) -> None:

        if self.width_m <= 0:
            raise ValueError(
                "Road width must be greater than zero"
            )

        if self.length_m <= 0:
            raise ValueError(
                "Road length must be greater than zero"
            )

