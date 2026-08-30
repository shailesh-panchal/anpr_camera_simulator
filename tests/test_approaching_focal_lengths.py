#!/usr/bin/env python3
"""Validate approaching vehicle with different focal lengths."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from generate_anpr_sequence import build_generator, build_parser


def test_approaching_focal_lengths():
    """Test approaching vehicle with different focal lengths."""
    
    focal_lengths = [12, 20, 55]
    
    print("Testing Approaching Vehicle with Different Focal Lengths")
    print("=" * 70)
    
    for focal_length_mm in focal_lengths:
        print(f"\n{'='*70}")
        print(f"Focal Length: {focal_length_mm}mm")
        print(f"{'='*70}")
        
        parser = build_parser()
        args = parser.parse_args([
            "--direction", "approaching",
            "--plate-number", f"KA{focal_length_mm:02d}FL1234",
            "--initial-distance-m", "30.0",
            "--focal-length-mm", str(focal_length_mm),
            "--include-vehicle",
            "--output", str(ROOT / "output" / f"car_approaching_fl{focal_length_mm}mm.mp4"),
            "--save-frames", str(ROOT / "output" / f"frames_approaching_fl{focal_length_mm}mm"),
        ])
        
        generator = build_generator(args)
        scenario = generator.scenario
        
        print(f"Camera Intrinsics:")
        print(f"  Focal Length (mm): {focal_length_mm}")
        print(f"  fx (pixels): {scenario.intrinsics.fx:.2f}")
        print(f"  fy (pixels): {scenario.intrinsics.fy:.2f}")
        print(f"  Principal Point: ({scenario.intrinsics.cx}, {scenario.intrinsics.cy})")
        print(f"\nGenerating {args.initial_distance_m}m → 0m approach sequence:")
        
        # Generate and display frame data at different distances
        frame_data_list = []
        for i, frame in enumerate(generator.generate()):
            frame_data_list.append(frame)
            if len(frame_data_list) >= 4:
                break
        
        # Show samples from start, early, middle, and end
        sample_indices = [0, len(frame_data_list)//3, 2*len(frame_data_list)//3, -1]
        
        for idx in sample_indices:
            if idx < len(frame_data_list):
                frame = frame_data_list[idx]
                dist = frame.vehicle_state.z_m
                plate_w = frame.projected_plate.width_pixels
                plate_h = frame.projected_plate.height_pixels
                plate_x = frame.projected_plate.top_left.u
                plate_y = frame.projected_plate.top_left.v
                
                print(f"  Distance: {dist:6.2f}m | Plate: ({plate_x:7.1f}, {plate_y:7.1f}) | Size: {plate_w:6.1f}×{plate_h:5.1f}px")
        
        # Generate full video
        from generate_anpr_sequence import generate_video
        output_path = generate_video(args)
        print(f"\n✓ Video saved: {output_path}")


if __name__ == "__main__":
    test_approaching_focal_lengths()
