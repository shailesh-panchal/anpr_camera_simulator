#!/usr/bin/env python3
"""Generate a short ANPR video sequence from the synthetic simulation pipeline."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from anpr_simulator.camera.config_loader import load_camera
from anpr_simulator.geometry.camera_intrinsics import CameraIntrinsics, create_camera_intrinsics
from anpr_simulator.geometry.camera_pose import CameraPose
from anpr_simulator.geometry.license_plate import LicensePlateDimensions
from anpr_simulator.geometry.vehicle import VehicleDimensions
from anpr_simulator.geometry.vehicle_trajectory import (
    VehicleDirection,
    VehicleTrajectory,
)
from anpr_simulator.renderer.opencv_renderer.renderer import add_road_background
from anpr_simulator.simulation.frame_generator import FrameGenerator


def parse_direction(value: str | VehicleDirection) -> VehicleDirection:
    if isinstance(value, VehicleDirection):
        return value

    normalized = str(value).strip().lower()
    if normalized in {"approaching", "approaching_camera", "towards_camera"}:
        return VehicleDirection.APPROACHING_CAMERA
    if normalized in {"away", "moving_away", "receding"}:
        return VehicleDirection.MOVING_AWAY
    raise argparse.ArgumentTypeError(
        "direction must be one of: approaching, moving_away"
    )


def resolve_camera_settings(args: argparse.Namespace) -> argparse.Namespace:
    config_path = Path(args.camera_config).expanduser().resolve() if args.camera_config else None
    camera = None

    if config_path is not None and config_path.exists():
        camera = load_camera(str(config_path))
    elif not config_path or not config_path.exists():
        default_path = ROOT / "config" / "cameras" / "satatya_cibr20mvl12cwp_p2.yaml"
        if default_path.exists():
            camera = load_camera(str(default_path))

    if camera is None:
        return args

    selected_fov = (
        camera.fov_range_config.tele if args.fov_mode == "tele" else camera.fov_range_config.wide
    )

    if args.frame_width is None:
        args.frame_width = camera.sensor_config.resolution.width
    if args.frame_height is None:
        args.frame_height = camera.sensor_config.resolution.height
    if args.fps is None:
        args.fps = float(camera.fps_config.max)
    if args.shutter_speed_s is None:
        args.shutter_speed_s = camera.shutter_config.min_speed
    if args.focal_length_mm is None:
        args.focal_length_mm = selected_fov.focal_length_mm

    intrinsics = create_camera_intrinsics(
        focal_length_mm=args.focal_length_mm,
        active_pixel_width=camera.sensor_config.active_pixel.width,
        active_pixel_height=camera.sensor_config.active_pixel.height,
        active_area_width_mm=camera.sensor_config.active_area.width,
        active_area_height_mm=camera.sensor_config.active_area.height,
    )

    args.fx = args.fx if args.fx is not None else intrinsics.fx
    args.fy = args.fy if args.fy is not None else intrinsics.fy
    args.cx = args.cx if args.cx is not None else intrinsics.cx
    args.cy = args.cy if args.cy is not None else intrinsics.cy

    return args


def build_generator(args: argparse.Namespace) -> FrameGenerator:
    args = resolve_camera_settings(args)
    direction = parse_direction(args.direction)

    intrinsics = CameraIntrinsics(
        fx=args.fx,
        fy=args.fy,
        cx=args.cx,
        cy=args.cy,
    )

    camera_pose = CameraPose(
        x_m=0.0,
        y_m=args.camera_height_m,
        z_m=0.0,
        pitch_deg=args.camera_pitch_deg,
    )

    vehicle_dimensions = VehicleDimensions(
        length_m=args.vehicle_length_m,
        width_m=args.vehicle_width_m,
        height_m=args.vehicle_height_m,
        license_plate_height_m=args.plate_mount_height_m,
    )

    plate_dimensions = LicensePlateDimensions(
        width_m=args.plate_width_m,
        height_m=args.plate_height_m,
    )

    trajectory = VehicleTrajectory(
        initial_z_m=args.initial_distance_m,
        speed_mps=args.speed_mps,
        x_m=0.0,
        y_m=0.0,
        direction=direction,
    )

    return FrameGenerator(
        fps=args.fps,
        duration_s=args.duration_s,
        trajectory=trajectory,
        vehicle_dimensions=vehicle_dimensions,
        plate_dimensions=plate_dimensions,
        camera_pose=camera_pose,
        intrinsics=intrinsics,
    )


def save_frames(args: argparse.Namespace, generator: FrameGenerator, width: int, height: int) -> int:
    frame_dir = Path(args.save_frames).expanduser().resolve()
    frame_dir.mkdir(parents=True, exist_ok=True)

    output_count = 0
    include_background = args.include_background and not args.plate_only
    include_vehicle = args.include_vehicle and not args.plate_only

    for index, rendered in enumerate(
        generator.generate_rendered(
            plate_number=args.plate_number,
            frame_size=(width, height),
            vehicle_size=(args.vehicle_render_width_px, args.vehicle_render_height_px),
            background_color=args.background_color,
            vehicle_color=args.vehicle_color,
            plate_background_color=args.plate_background_color,
            plate_text_color=args.plate_text_color,
            include_background=include_background,
            include_vehicle=include_vehicle,
        )
    ):
        if args.frame_format == "png":
            filename = frame_dir / f"frame_{index:05d}.png"
            cv2.imwrite(str(filename), rendered)
        elif args.frame_format == "yuv420":
            filename = frame_dir / f"frame_{index:05d}.yuv"
            yuv = cv2.cvtColor(rendered, cv2.COLOR_BGR2YUV_I420)
            with open(filename, "wb") as handle:
                handle.write(yuv.tobytes())
        else:
            raise ValueError(f"Unsupported frame format: {args.frame_format}")

        output_count += 1

    print(f"Saved {output_count} frames to {frame_dir} ({args.frame_format})")
    return output_count


def generate_video(args: argparse.Namespace) -> Path:
    generator = build_generator(args)

    output_path = Path(args.output).expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    width, height = args.frame_width, args.frame_height

    if args.save_frames:
        save_frames(args, generator, width, height)

    if not args.output:
        return output_path

    writer = cv2.VideoWriter(
        str(output_path),
        cv2.VideoWriter_fourcc(*"mp4v"),
        args.fps,
        (width, height),
    )

    if not writer.isOpened():
        raise RuntimeError(
            f"Failed to open video writer for output: {output_path}"
        )

    include_background = args.include_background and not args.plate_only
    include_vehicle = args.include_vehicle and not args.plate_only

    frame_count = 0
    for rendered in generator.generate_rendered(
        plate_number=args.plate_number,
        frame_size=(width, height),
        vehicle_size=(args.vehicle_render_width_px, args.vehicle_render_height_px),
        background_color=args.background_color,
        vehicle_color=args.vehicle_color,
        plate_background_color=args.plate_background_color,
        plate_text_color=args.plate_text_color,
        include_background=include_background,
        include_vehicle=include_vehicle,
    ):
        writer.write(rendered)
        frame_count += 1

    writer.release()

    print(
        f"Generated {frame_count} frames at {args.fps} FPS -> {output_path}"
    )
    return output_path


def _parse_color(value: str) -> tuple[int, int, int]:
    parts = [int(part.strip()) for part in value.split(",")]
    if len(parts) != 3:
        raise argparse.ArgumentTypeError(
            "Color must be in B,G,R format like '0,0,0' or '255,255,255'"
        )
    return tuple(parts)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a short synthetic ANPR video from camera geometry and render logic."
    )

    parser.add_argument("--plate-number", default="KA01AB1234", help="Plate text to render.")
    parser.add_argument("--direction", default="approaching", type=parse_direction,
                        help="Vehicle direction: approaching or moving_away")

    parser.add_argument("--camera-config", default=str(ROOT / "config" / "cameras" / "satatya_cibr20mvl12cwp_p2.yaml"),
                        help="YAML camera configuration file to use for focal length, sensor size, FOV, FPS, and shutter settings.")
    parser.add_argument("--camera-height-m", type=float, default=2.0,
                        help="Camera height above road in meters.")
    parser.add_argument("--camera-pitch-deg", type=float, default=10.0,
                        help="Camera pitch angle in degrees.")
    parser.add_argument("--fov-mode", choices=["wide", "tele"], default="wide",
                        help="Camera FOV preset to use when deriving the lens focal length from the YAML config.")
    parser.add_argument("--focal-length-mm", type=float, default=None,
                        help="Override focal length in millimeters. If omitted, the selected FOV mode from the camera config is used.")

    parser.add_argument("--frame-width", type=int, default=None, help="Output frame width in pixels. If omitted, the camera config resolution is used.")
    parser.add_argument("--frame-height", type=int, default=None, help="Output frame height in pixels. If omitted, the camera config resolution is used.")

    parser.add_argument("--vehicle-length-m", type=float, default=4.2,
                        help="Typical Indian compact sedan length in meters.")
    parser.add_argument("--vehicle-width-m", type=float, default=1.8,
                        help="Typical Indian four-wheel vehicle width in meters.")
    parser.add_argument("--vehicle-height-m", type=float, default=1.6,
                        help="Typical Indian four-wheel vehicle height in meters.")
    parser.add_argument("--plate-mount-height-m", type=float, default=0.5,
                        help="Vertical offset of the plate from vehicle ground.")

    parser.add_argument("--plate-width-m", type=float, default=0.52,
                        help="Indian registration plate width in meters (approx. 520 mm).")
    parser.add_argument("--plate-height-m", type=float, default=0.11,
                        help="Indian registration plate height in meters (approx. 110 mm).")

    parser.add_argument("--speed-mps", type=float, default=2.7777777778,
                        help="Vehicle speed in meters per second (10 km/h typical city speed).")
    parser.add_argument("--initial-distance-m", type=float, default=30.0,
                        help="Initial vehicle distance from camera in meters.")
    parser.add_argument("--duration-s", type=float, default=2.0,
                        help="Video duration in seconds.")
    parser.add_argument("--fps", type=float, default=None,
                        help="Output video FPS. If omitted, the camera config FPS max value is used.")
    parser.add_argument("--shutter-speed-s", type=float, default=None,
                        help="Exposure shutter speed in seconds. If omitted, the camera config min shutter value is used.")

    parser.add_argument("--fx", type=float, default=None,
                        help="Camera focal length in pixels along X. If omitted, it is derived from the camera config.")
    parser.add_argument("--fy", type=float, default=None,
                        help="Camera focal length in pixels along Y. If omitted, it is derived from the camera config.")
    parser.add_argument("--cx", type=float, default=None,
                        help="Image center x coordinate in pixels. If omitted, it is derived from the sensor size.")
    parser.add_argument("--cy", type=float, default=None,
                        help="Image center y coordinate in pixels. If omitted, it is derived from the sensor size.")

    parser.add_argument("--vehicle-render-width-px", type=int, default=260,
                        help="Rendered vehicle rectangle width in pixels.")
    parser.add_argument("--vehicle-render-height-px", type=int, default=110,
                        help="Rendered vehicle rectangle height in pixels.")

    parser.add_argument("--background-color", type=_parse_color, default=(30, 30, 30),
                        help="Background B,G,R triple, e.g. '30,30,30'.")
    parser.add_argument("--vehicle-color", type=_parse_color, default=(80, 80, 80),
                        help="Vehicle B,G,R triple, e.g. '80,80,80'.")
    parser.add_argument("--plate-background-color", type=_parse_color, default=(255, 255, 255),
                        help="Plate background B,G,R triple.")
    parser.add_argument("--plate-text-color", type=_parse_color, default=(0, 0, 0),
                        help="Plate text B,G,R triple.")
    parser.add_argument("--plate-only", action="store_true",
                        help="Render only the projected license plate on a flat background; road and vehicle are excluded.")
    parser.add_argument("--include-background", action=argparse.BooleanOptionalAction, default=False,
                        help="Include the road background in the rendered frame.")
    parser.add_argument("--include-vehicle", action=argparse.BooleanOptionalAction, default=False,
                        help="Include the rendered vehicle silhouette in the scene.")

    parser.add_argument("--output", default=str(ROOT / "output" / "anpr_sequence.mp4"),
                        help="Output video path.")
    parser.add_argument("--save-frames", default=None,
                        help="Directory to save extracted frames. Supported formats: PNG and YUV420 raw.")
    parser.add_argument("--frame-format", choices=["png", "yuv420"], default="png",
                        help="Format used when --save-frames is set.")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    try:
        generate_video(args)
    except Exception as exc:  # pragma: no cover
        raise SystemExit(f"Failed to generate video: {exc}") from exc


if __name__ == "__main__":
    main()
