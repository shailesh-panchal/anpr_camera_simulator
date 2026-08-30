#!/usr/bin/env python3
"""Debug test: Visualize vehicle and plate coordinate alignment."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import cv2
from generate_anpr_sequence import build_generator, build_parser


def test_vehicle_plate_alignment():
    """Debug vehicle and plate alignment."""
    
    parser = build_parser()
    args = parser.parse_args([
        "--direction", "moving_away",
        "--plate-number", "KA01AB5678",
        "--initial-distance-m", "3.0",
        "--include-vehicle",
        "--output", str(ROOT / "output" / "car_moving_away_debug.mp4"),
    ])
    
    print("Vehicle and Plate Alignment Debug")
    print("=" * 60)
    
    generator = build_generator(args)
    
    for i, frame_data in enumerate(generator.generate()):
        if i >= 3:
            break
        
        # Get vehicle state
        vehicle_state = frame_data.vehicle_state
        projected_plate = frame_data.projected_plate
        
        print(f"\nFrame {i}:")
        print(f"  Vehicle State:")
        print(f"    Position (X, Y, Z): ({vehicle_state.x_m:.3f}, {vehicle_state.y_m:.3f}, {vehicle_state.z_m:.3f})")
        print(f"  Projected Plate:")
        print(f"    Top-Left:     ({projected_plate.top_left.u:.1f}, {projected_plate.top_left.v:.1f})")
        print(f"    Top-Right:    ({projected_plate.top_right.u:.1f}, {projected_plate.top_right.v:.1f})")
        print(f"    Bottom-Left:  ({projected_plate.bottom_left.u:.1f}, {projected_plate.bottom_left.v:.1f})")
        print(f"    Bottom-Right: ({projected_plate.bottom_right.u:.1f}, {projected_plate.bottom_right.v:.1f})")
        print(f"    Size: {projected_plate.width_pixels:.1f}px x {projected_plate.height_pixels:.1f}px")
    
    # Now generate actual rendered frames for visual inspection
    print("\n" + "=" * 60)
    print("Generating rendered frames with annotations...")
    
    generator = build_generator(args)
    
    for i, rendered in enumerate(generator.generate_rendered(
        plate_number=args.plate_number,
        frame_size=(args.frame_width, args.frame_height),
        include_vehicle=True,
        include_background=True,
    )):
        if i >= 3:
            break
        
        # Save frame with coordinates shown
        output_path = ROOT / "output" / f"debug_frame_{i:03d}.png"
        cv2.imwrite(str(output_path), rendered)
        print(f"  Saved frame {i}: {output_path}")


if __name__ == "__main__":
    test_vehicle_plate_alignment()
