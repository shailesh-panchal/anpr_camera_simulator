#!/usr/bin/env python3
"""Visual test: Overlay vehicle and plate bounds with annotations."""

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
from anpr_simulator.geometry.transform import world_to_camera
from anpr_simulator.geometry.projection import project_point
from anpr_simulator.geometry.world import WorldPoint


def test_with_annotations():
    """Render with vehicle and plate bounding boxes annotated."""
    
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
    
    for i, (frame_data, rendered) in enumerate(zip(generator.generate(), 
                                                   generator.generate_rendered(
                                                       plate_number=args.plate_number,
                                                       frame_size=(args.frame_width, args.frame_height),
                                                       include_vehicle=True,
                                                       include_background=True,
                                                   ))):
        if i >= 1:
            break
        
        # Get data
        vehicle_state = frame_data.vehicle_state
        projected_plate = frame_data.projected_plate
        
        # Project vehicle corners
        half_length = scenario.vehicle_dimensions.length_m / 2.0
        half_width = scenario.vehicle_dimensions.width_m / 2.0
        total_height = scenario.vehicle_dimensions.height_m
        
        # Bottom corners (ground level Y=0)
        bottom_corners = [
            WorldPoint(x_m=vehicle_state.x_m - half_width, y_m=0.0, z_m=vehicle_state.z_m - half_length),
            WorldPoint(x_m=vehicle_state.x_m + half_width, y_m=0.0, z_m=vehicle_state.z_m - half_length),
            WorldPoint(x_m=vehicle_state.x_m + half_width, y_m=0.0, z_m=vehicle_state.z_m + half_length),
            WorldPoint(x_m=vehicle_state.x_m - half_width, y_m=0.0, z_m=vehicle_state.z_m + half_length),
        ]
        
        # Top corners (roof level Y=total_height)
        top_corners = [
            WorldPoint(x_m=vehicle_state.x_m - half_width, y_m=total_height, z_m=vehicle_state.z_m - half_length),
            WorldPoint(x_m=vehicle_state.x_m + half_width, y_m=total_height, z_m=vehicle_state.z_m - half_length),
            WorldPoint(x_m=vehicle_state.x_m + half_width, y_m=total_height, z_m=vehicle_state.z_m + half_length),
            WorldPoint(x_m=vehicle_state.x_m - half_width, y_m=total_height, z_m=vehicle_state.z_m + half_length),
        ]
        
        # Plate corners
        plate_tl = int(projected_plate.top_left.u), int(projected_plate.top_left.v)
        plate_tr = int(projected_plate.top_right.u), int(projected_plate.top_right.v)
        plate_bl = int(projected_plate.bottom_left.u), int(projected_plate.bottom_left.v)
        plate_br = int(projected_plate.bottom_right.u), int(projected_plate.bottom_right.v)
        
        # Draw on rendered frame
        frame = rendered.copy()
        
        # Draw vehicle bottom corners
        for corner in bottom_corners:
            cam_pt = world_to_camera(corner, scenario.camera_pose)
            img_pt = project_point(cam_pt, scenario.intrinsics)
            pt = (int(img_pt.u), int(img_pt.v))
            if 0 <= pt[0] < frame.shape[1] and 0 <= pt[1] < frame.shape[0]:
                cv2.circle(frame, pt, 5, (0, 255, 0), -1)  # Green bottom
        
        # Draw vehicle top corners  
        for corner in top_corners:
            cam_pt = world_to_camera(corner, scenario.camera_pose)
            img_pt = project_point(cam_pt, scenario.intrinsics)
            pt = (int(img_pt.u), int(img_pt.v))
            if 0 <= pt[0] < frame.shape[1] and 0 <= pt[1] < frame.shape[0]:
                cv2.circle(frame, pt, 5, (255, 0, 0), -1)  # Blue top
        
        # Draw vehicle panel outline (back panel for moving away)
        back_panel_pts = []
        for corner in [bottom_corners[2], bottom_corners[3], top_corners[3], top_corners[2]]:
            cam_pt = world_to_camera(corner, scenario.camera_pose)
            img_pt = project_point(cam_pt, scenario.intrinsics)
            back_panel_pts.append([int(img_pt.u), int(img_pt.v)])
        
        if back_panel_pts:
            back_panel_pts = np.array(back_panel_pts, dtype=np.int32)
            cv2.polylines(frame, [back_panel_pts], True, (100, 100, 255), 3)  # Red back panel
        
        # Draw plate box
        cv2.rectangle(frame, plate_tl, plate_br, (0, 165, 255), 3)  # Orange plate box
        
        # Add labels
        cv2.putText(frame, "Vehicle Bottom (Green)", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, "Vehicle Top (Blue)", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        cv2.putText(frame, "Vehicle Panel (Red)", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100, 100, 255), 2)
        cv2.putText(frame, "License Plate (Orange)", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 165, 255), 2)
        
        output_path = ROOT / "output" / "vehicle_plate_overlay.png"
        cv2.imwrite(str(output_path), frame)
        print(f"Saved annotated frame: {output_path}")


if __name__ == "__main__":
    test_with_annotations()
