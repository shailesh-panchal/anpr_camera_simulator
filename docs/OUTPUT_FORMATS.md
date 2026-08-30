# Output Formats

## Overview

The simulator can emit both abstract simulation results and rendered image outputs.

## Simulation outputs

Simulation output is a `SimulationFrame` or aggregated `SimulationResult` object.

These outputs are optimized for analysis, not direct display.

## Image outputs

### PNG

PNG is useful for debugging, inspection, and static frame export.

### YUV420 raw

YUV420 raw format is useful when testing camera pipelines, image processing stacks, or lower-level video processing where planar YUV data is required.

The script writes a `.yuv` file containing the YUV420 image data.

### MP4

MP4 is useful for video playback and sequence review.

## Script support

The output script supports:

- `--output` for MP4
- `--save-frames` for directory-based frame export
- `--frame-format png|yuv420`

Main file:

- [generate_anpr_sequence.py](../generate_anpr_sequence.py)

## Recommended usage

- Use PNG for visual debugging
- Use YUV420 for low-level pipeline validation
- Use MP4 for quick review of the motion sequence
- Use geometric simulation when you do not need image output
