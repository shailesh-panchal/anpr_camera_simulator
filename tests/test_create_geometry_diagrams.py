#!/usr/bin/env python3
"""Create visual diagram of camera geometry and vehicle motion."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from generate_anpr_sequence import build_generator, build_parser
import cv2
import numpy as np


def create_geometry_diagram():
    """Create a side-view diagram showing camera geometry."""
    
    # Create a blank image
    img = np.ones((600, 1000, 3), dtype=np.uint8) * 255
    
    print("Creating camera geometry diagram...")
    
    # Draw ground line
    cv2.line(img, (50, 500), (950, 500), (0, 0, 0), 2)
    cv2.putText(img, "ROAD (Y=0m)", (50, 525), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
    
    # Draw camera position
    camera_x = 50
    camera_y = 150  # 2m above road at pixel scale
    cv2.circle(img, (camera_x, camera_y), 8, (0, 0, 255), -1)
    cv2.putText(img, "CAMERA (Y=2.0m)", (camera_x+15, camera_y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    
    # Draw camera pitch line (10 degrees down)
    pitch_angle = np.radians(10)
    pitch_length = 400
    pitch_x = camera_x + pitch_length * np.cos(pitch_angle)
    pitch_y = camera_y + pitch_length * np.sin(pitch_angle)
    cv2.line(img, (camera_x, camera_y), (int(pitch_x), int(pitch_y)), (0, 0, 255), 2)
    cv2.putText(img, "Camera Pitch: -10°", (camera_x+20, camera_y+40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    
    # Draw vehicles at different distances
    vehicles = [
        (850, "30m away", (255, 100, 100)),
        (650, "16m away", (100, 200, 100)),
        (400, "4m away", (100, 100, 255)),
    ]
    
    for x, label, color in vehicles:
        cv2.rectangle(img, (x-30, 475), (x+30, 500), color, -1)
        cv2.putText(img, label, (x-60, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
    
    # Draw arrows showing vertical motion
    arrow_y_start = 550
    for i, (x, _, color) in enumerate(vehicles):
        arrow_y = arrow_y_start + i*40
        if i < len(vehicles) - 1:
            cv2.arrowedLine(img, (vehicles[i][0], arrow_y), (vehicles[i+1][0], arrow_y), (0, 200, 0), 2)
    
    cv2.putText(img, "VEHICLE APPROACHES: Moves UP in image (bottom -> top)", 
                (100, 580), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 150, 0), 2)
    
    # Add coordinate system
    cv2.putText(img, "Side View (Camera Looking Down)", (300, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
    
    output_path = ROOT / "output" / "camera_geometry_diagram.png"
    cv2.imwrite(str(output_path), img)
    print(f"✓ Saved: {output_path}")


def create_image_plane_diagram():
    """Create a diagram showing image plane with vehicle positions."""
    
    img = np.ones((600, 800, 3), dtype=np.uint8) * 255
    
    # Draw frame boundaries
    cv2.rectangle(img, (100, 50), (700, 550), (0, 0, 0), 2)
    cv2.putText(img, "Image Plane (What Camera Sees)", (200, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
    
    # Add distance labels
    cv2.putText(img, "Approaching Vehicle Path:", (120, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    
    # Vehicle positions in image (showing vertical motion)
    positions = [
        (150, 500, "30m away\n(Bottom of frame)", (255, 100, 100)),
        (300, 380, "16m away\n(Middle-low)", (100, 200, 100)),
        (450, 260, "8m away\n(Middle)", (100, 150, 200)),
        (600, 120, "2m away\n(Top of frame)", (100, 100, 255)),
    ]
    
    # Draw vehicle icons and motion arrows
    for i, (x, y, label, color) in enumerate(positions):
        # Draw vehicle
        cv2.rectangle(img, (x-25, y-15), (x+25, y+15), color, -1)
        cv2.rectangle(img, (x-25, y-15), (x+25, y+15), (0, 0, 0), 1)
        
        # Draw arrow showing motion
        if i > 0:
            prev_x, prev_y = positions[i-1][0], positions[i-1][1]
            cv2.arrowedLine(img, (prev_x, prev_y), (x, y), (0, 150, 0), 2)
        
        # Draw label
        cv2.putText(img, label, (x-40, y-40), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1)
    
    # Add annotations
    cv2.putText(img, "Vehicle moves: DOWN -> UP", (120, 580), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 150, 0), 2)
    cv2.putText(img, "(Image V-coordinate DECREASES)", (120, 600), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 150, 0), 1)
    
    output_path = ROOT / "output" / "image_plane_vehicle_motion.png"
    cv2.imwrite(str(output_path), img)
    print(f"✓ Saved: {output_path}")


if __name__ == "__main__":
    create_geometry_diagram()
    create_image_plane_diagram()
    print("\n✓ Diagrams created successfully!")
