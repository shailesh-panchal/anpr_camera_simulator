#!/usr/bin/env python3
"""Test script: Vehicle approaching from LEFT side of center."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from generate_anpr_sequence import build_generator, build_parser


def test_car_approaching_left_side():
    """Generate a video of a car approaching from the left side of center."""
    
    parser = build_parser()
    args = parser.parse_args([
        "--direction", "approaching",
        "--plate-number", "KA03LF1234",  # LF = Left side
        "--initial-distance-m", "30.0",
        "--include-vehicle",
        "--include-background",
        "--output", str(ROOT / "output" / "car_approaching_left.mp4"),
        "--save-frames", str(ROOT / "output" / "frames_approaching_left"),
    ])
    
    print("Testing Car Approaching from LEFT Side of Center")
    print("=" * 70)
    
    generator = build_generator(args)
    scenario = generator.scenario
    
    print(f"Configuration:")
    print(f"  Direction: {args.direction}")
    print(f"  Plate: {args.plate_number}")
    print(f"  Initial distance: {args.initial_distance_m}m")
    print(f"  Speed: {args.speed_mps:.2f} m/s")
    print(f"  Duration: ~{args.initial_distance_m / args.speed_mps:.2f} seconds")
    print(f"  Camera height: {scenario.camera_pose.y_m}m")
    print(f"  Camera pitch: {scenario.camera_pose.pitch_deg}°")
    
    # Generate and display first few frames info
    print(f"\nFrame Data (Vehicle on LEFT side):")
    print(f"{'Frame':>5} | {'Distance':>8} | {'Vehicle X':>10} | {'Plate X':>8} | {'Plate Y':>8} | {'Plate Size':>12}")
    print(f"{'-'*5}-+-{'-'*8}-+-{'-'*10}-+-{'-'*8}-+-{'-'*8}-+-{'-'*12}")
    
    frame_data_list = []
    for i, frame in enumerate(generator.generate()):
        frame_data_list.append(frame)
        if len(frame_data_list) <= 5 or (i > 0 and i % 50 == 0) or i >= len(list(generator.generate())) - 3:
            dist = frame.vehicle_state.z_m
            x_m = frame.vehicle_state.x_m
            plate_x = frame.projected_plate.top_left.u
            plate_y = frame.projected_plate.top_left.v
            plate_w = frame.projected_plate.width_pixels
            plate_h = frame.projected_plate.height_pixels
            
            print(f"{i:5d} | {dist:8.2f}m | {x_m:10.2f}m | {plate_x:8.1f} | {plate_y:8.1f} | {plate_w:6.1f}x{plate_h:5.1f}px")
    
    # Now generate the actual video
    from generate_anpr_sequence import generate_video
    output_path = generate_video(args)
    print(f"\n✓ Video generated: {output_path}")


if __name__ == "__main__":
    test_car_approaching_left_side()
