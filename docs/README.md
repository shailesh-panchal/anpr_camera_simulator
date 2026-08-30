# ANPR Simulator Documentation

This folder contains the design and reference documents for the ANPR camera simulator project.

## Documents

- [ANPR_SIMULATOR_DESIGN.md](ANPR_SIMULATOR_DESIGN.md) — main architecture and implementation overview

## Overview

The simulator creates synthetic ANPR sequences by combining:

- 3D vehicle trajectory and plate geometry
- camera pose and intrinsic projection
- OpenCV-based rendering of the plate and vehicle
- time-stepped frame generation according to FPS and vehicle speed

The project is intended to support synthetic video generation for ANPR testing and evaluation workflows.
