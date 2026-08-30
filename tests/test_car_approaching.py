#!/usr/bin/env python3
"""Test script: Generate ANPR video with car moving towards camera."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from generate_anpr_sequence import build_generator, build_parser


def test_car_approaching():
    """Generate a video of a car approaching the camera."""
    
    # Parse default arguments and override direction
    parser = build_parser()
    args = parser.parse_args([
        "--direction", "approaching",
        "--plate-number", "KA02CD9876",
        "--initial-distance-m", "30.0",  # Start far from camera, approach towards it
        "--include-vehicle",
        "--output", str(ROOT / "output" / "car_approaching.mp4"),
        "--save-frames", str(ROOT / "output" / "frames_approaching"),
    ])
    
    print(f"Testing car approaching camera...")
    print(f"  Direction: {args.direction}")
    print(f"  Plate: {args.plate_number}")
    print(f"  Initial distance: {args.initial_distance_m} m")
    print(f"  Speed: {args.speed_mps} m/s")
    print(f"  Duration: ~{args.initial_distance_m / args.speed_mps:.2f} seconds")
    
    generator = build_generator(args)
    
    # Generate and display first few frames info
    for i, frame in enumerate(generator.generate()):
        if i < 3:
            print(f"  Frame {i}: Plate position: ({frame.projected_plate.top_left.u:.1f}, {frame.projected_plate.top_left.v:.1f}), "
                  f"Size: {frame.projected_plate.width_pixels:.1f}px x {frame.projected_plate.height_pixels:.1f}px")
        if i >= 3:
            break
    
    # Now generate the actual video
    from generate_anpr_sequence import generate_video
    output_path = generate_video(args)
    print(f"\n✓ Video generated: {output_path}")


if __name__ == "__main__":
    test_car_approaching()
