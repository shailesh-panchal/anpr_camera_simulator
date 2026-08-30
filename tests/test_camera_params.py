#!/usr/bin/env python3
"""Check actual camera parameters being used."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from generate_anpr_sequence import build_generator, build_parser


def test_camera_params():
    """Print actual camera parameters."""
    
    parser = build_parser()
    args = parser.parse_args([
        "--direction", "moving_away",
        "--initial-distance-m", "3.0",
    ])
    
    generator = build_generator(args)
    scenario = generator.scenario
    
    print("Camera Parameters")
    print("=" * 60)
    print(f"Camera Intrinsics:")
    print(f"  fx (X focal length): {scenario.intrinsics.fx}")
    print(f"  fy (Y focal length): {scenario.intrinsics.fy}")
    print(f"  cx (X center):       {scenario.intrinsics.cx}")
    print(f"  cy (Y center):       {scenario.intrinsics.cy}")
    print(f"\nCamera Pose:")
    print(f"  Position: ({scenario.camera_pose.x_m}, {scenario.camera_pose.y_m}, {scenario.camera_pose.z_m})")
    print(f"  Pitch:    {scenario.camera_pose.pitch_deg} degrees")
    print(f"\nVehicle Dimensions:")
    print(f"  Length:          {scenario.vehicle_dimensions.length_m}m")
    print(f"  Width:           {scenario.vehicle_dimensions.width_m}m")
    print(f"  Height:          {scenario.vehicle_dimensions.height_m}m")
    print(f"  Plate mount height: {scenario.vehicle_dimensions.license_plate_height_m}m")
    print(f"\nPlate Dimensions:")
    print(f"  Width:           {scenario.plate_dimensions.width_m}m")
    print(f"  Height:          {scenario.plate_dimensions.height_m}m")


if __name__ == "__main__":
    test_camera_params()
