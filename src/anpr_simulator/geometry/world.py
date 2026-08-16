from dataclasses import dataclass


@dataclass(frozen=True)
class WorldPoint:
    """
    Point in the world/road coordinate system.

    x_m:
        Lateral position.

    y_m:
        Height above road.

    z_m:
        Distance along road.
    """

    x_m: float
    y_m: float
    z_m: float