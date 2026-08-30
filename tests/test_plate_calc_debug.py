#!/usr/bin/env python3
"""Detailed debugging of plate coordinate calculation."""

import sys
from pathlib import Path
import math

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from generate_anpr_sequence import build_generator, build_parser
from anpr_simulator.geometry.transform import world_to_camera
from anpr_simulator.geometry.projection import project_point
from anpr_simulator.geometry.world import WorldPoint
from anpr_simulator.geometry.license_plate import license_plate_corners


def test_detailed_plate_calc():
    """Step-by-step plate projection debugging."""
    
    parser = build_parser()
    args = parser.parse_args([
        "--direction", "moving_away",
        "--initial-distance-m", "3.0",
    ])
    
    generator = build_generator(args)
    scenario = generator.scenario
    
    for i, frame_data in enumerate(generator.generate()):
        if i >= 1:
            break
        
        vehicle_state = frame_data.vehicle_state
        
        print("=" * 70)
        print("DETAILED PLATE PROJECTION CALCULATION")
        print("=" * 70)
        print(f"\nVehicle State:")
        print(f"  X: {vehicle_state.x_m}, Y: {vehicle_state.y_m}, Z: {vehicle_state.z_m}")
        
        # Calculate plate corners in world coordinates
        half_width = scenario.plate_dimensions.width_m / 2.0
        half_height = scenario.plate_dimensions.height_m / 2.0
        
        print(f"\nPlate Dimensions:")
        print(f"  Width: {scenario.plate_dimensions.width_m}m, Height: {scenario.plate_dimensions.height_m}m")
        print(f"  Half-width: {half_width}m, Half-height: {half_height}m")
        
        plate_corners = license_plate_corners(
            center_x_m=vehicle_state.x_m,
            center_y_m=vehicle_state.y_m,
            distance_z_m=vehicle_state.z_m,
            dimensions=scenario.plate_dimensions,
        )
        
        print(f"\nPlate Corners (World Coordinates):")
        corner_names = ["Top-Left", "Top-Right", "Bottom-Left", "Bottom-Right"]
        for name, corner in zip(corner_names, plate_corners):
            print(f"  {name:15s}: ({corner.x:7.3f}, {corner.y:7.3f}, {corner.z:7.3f})")
        
        print(f"\nCamera Parameters:")
        print(f"  Camera Pose: ({scenario.camera_pose.x_m}, {scenario.camera_pose.y_m}, {scenario.camera_pose.z_m})")
        print(f"  Pitch: {scenario.camera_pose.pitch_deg}°")
        print(f"  Intrinsics: fx={scenario.intrinsics.fx:.2f}, fy={scenario.intrinsics.fy:.2f}, cx={scenario.intrinsics.cx}, cy={scenario.intrinsics.cy}")
        
        print(f"\nTransformation to Camera Coordinates:")
        pitch_rad = math.radians(scenario.camera_pose.pitch_deg)
        cos_pitch = math.cos(pitch_rad)
        sin_pitch = math.sin(pitch_rad)
        
        for name, corner in zip(corner_names, plate_corners):
            # World to camera
            dx = corner.x - scenario.camera_pose.x_m
            dy = corner.y - scenario.camera_pose.y_m
            dz = corner.z - scenario.camera_pose.z_m
            
            x_cam = dx
            z_cam = cos_pitch * dz - sin_pitch * dy
            y_cam = -sin_pitch * dz - cos_pitch * dy
            
            print(f"  {name:15s}:")
            print(f"    Delta: dx={dx:7.3f}, dy={dy:7.3f}, dz={dz:7.3f}")
            print(f"    Camera: x={x_cam:7.3f}, y={y_cam:7.3f}, z={z_cam:7.3f}")
            
            # Project to image
            u = scenario.intrinsics.fx * x_cam / z_cam + scenario.intrinsics.cx
            v = scenario.intrinsics.cy - scenario.intrinsics.fy * y_cam / z_cam
            
            print(f"    Image:  u={u:7.1f}, v={v:7.1f}")
        
        # Compare with actual projected plate from frame data
        print(f"\nActual Projected Plate (from frame_data):")
        print(f"  Top-Left:     ({frame_data.projected_plate.top_left.u:7.1f}, {frame_data.projected_plate.top_left.v:7.1f})")
        print(f"  Top-Right:    ({frame_data.projected_plate.top_right.u:7.1f}, {frame_data.projected_plate.top_right.v:7.1f})")
        print(f"  Bottom-Left:  ({frame_data.projected_plate.bottom_left.u:7.1f}, {frame_data.projected_plate.bottom_left.v:7.1f})")
        print(f"  Bottom-Right: ({frame_data.projected_plate.bottom_right.u:7.1f}, {frame_data.projected_plate.bottom_right.v:7.1f})")


if __name__ == "__main__":
    test_detailed_plate_calc()
