#!/usr/bin/env python3
"""Debug test: Show vehicle corners and plate with annotations."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import cv2
import numpy as np
from generate_anpr_sequence import build_generator, build_parser
from anpr_simulator.geometry.vehicle_state import VehicleState
from anpr_simulator.geometry.transform import world_to_camera
from anpr_simulator.geometry.projection import project_point
from anpr_simulator.geometry.world import WorldPoint


def test_vehicle_plate_projection():
    """Show vehicle box and plate position together."""
    
    parser = build_parser()
    args = parser.parse_args([
        "--direction", "moving_away",
        "--plate-number", "KA01AB5678",
        "--initial-distance-m", "3.0",
        "--include-vehicle",
        "--output", str(ROOT / "output" / "temp.mp4"),
    ])
    
    generator = build_generator(args)
    scenario = generator.scenario
    
    print("Vehicle and Plate Projection Analysis")
    print("=" * 60)
    
    for i, frame_data in enumerate(generator.generate()):
        if i >= 1:
            break
        
        vehicle_state = frame_data.vehicle_state
        projected_plate = frame_data.projected_plate
        
        print(f"\nFrame {i}:")
        print(f"  Vehicle dimensions: {scenario.vehicle_dimensions.length_m}m x {scenario.vehicle_dimensions.width_m}m x {scenario.vehicle_dimensions.height_m}m")
        print(f"  Plate mount height: {scenario.vehicle_dimensions.license_plate_height_m}m")
        print(f"  Vehicle state Y (should be plate height): {vehicle_state.y_m}m")
        
        # Project vehicle corners
        half_length = scenario.vehicle_dimensions.length_m / 2.0
        half_width = scenario.vehicle_dimensions.width_m / 2.0
        total_height = scenario.vehicle_dimensions.height_m
        
        corners_3d = [
            (vehicle_state.x_m - half_width, 0.0, vehicle_state.z_m - half_length, "Front-Left-Bottom"),
            (vehicle_state.x_m + half_width, 0.0, vehicle_state.z_m - half_length, "Front-Right-Bottom"),
            (vehicle_state.x_m + half_width, 0.0, vehicle_state.z_m + half_length, "Back-Right-Bottom"),
            (vehicle_state.x_m - half_width, 0.0, vehicle_state.z_m + half_length, "Back-Left-Bottom"),
            (vehicle_state.x_m - half_width, total_height, vehicle_state.z_m - half_length, "Front-Left-Top"),
            (vehicle_state.x_m + half_width, total_height, vehicle_state.z_m - half_length, "Front-Right-Top"),
            (vehicle_state.x_m + half_width, total_height, vehicle_state.z_m + half_length, "Back-Right-Top"),
            (vehicle_state.x_m - half_width, total_height, vehicle_state.z_m + half_length, "Back-Left-Top"),
        ]
        
        print(f"\n  Vehicle corners (world coordinates):")
        projected_corners = []
        for x_m, y_m, z_m, label in corners_3d:
            world_pt = WorldPoint(x_m=x_m, y_m=y_m, z_m=z_m)
            cam_pt = world_to_camera(world_pt, scenario.camera_pose)
            img_pt = project_point(cam_pt, scenario.intrinsics)
            projected_corners.append((img_pt.u, img_pt.v, label, y_m))
            if y_m == 0.0 or y_m == total_height:
                print(f"    {label:20s}: World({x_m:6.3f}, {y_m:6.3f}, {z_m:6.3f}) -> Image({img_pt.u:7.1f}, {img_pt.v:7.1f})")
        
        print(f"\n  Plate corners (world Y = {vehicle_state.y_m}m):")
        print(f"    Top-Left:     Image({projected_plate.top_left.u:7.1f}, {projected_plate.top_left.v:7.1f})")
        print(f"    Top-Right:    Image({projected_plate.top_right.u:7.1f}, {projected_plate.top_right.v:7.1f})")
        print(f"    Bottom-Left:  Image({projected_plate.bottom_left.u:7.1f}, {projected_plate.bottom_left.v:7.1f})")
        print(f"    Bottom-Right: Image({projected_plate.bottom_right.u:7.1f}, {projected_plate.bottom_right.v:7.1f})")
        
        # Check if plate should be inside vehicle bounds
        min_y_vehicle = min(c[1] for c in projected_corners if c[3] in [0.0, total_height])
        max_y_vehicle = max(c[1] for c in projected_corners if c[3] in [0.0, total_height])
        plate_min_y = min(projected_plate.top_left.v, projected_plate.top_right.v)
        plate_max_y = max(projected_plate.bottom_left.v, projected_plate.bottom_right.v)
        
        print(f"\n  Analysis:")
        print(f"    Vehicle Y range (projected): {min_y_vehicle:.1f} to {max_y_vehicle:.1f}")
        print(f"    Plate Y range (projected):   {plate_min_y:.1f} to {plate_max_y:.1f}")
        
        if plate_min_y < min_y_vehicle or plate_max_y > max_y_vehicle:
            print(f"    ⚠️  MISALIGNMENT: Plate is outside vehicle bounds!")
        else:
            print(f"    ✓ Plate is within vehicle bounds")


if __name__ == "__main__":
    test_vehicle_plate_projection()
