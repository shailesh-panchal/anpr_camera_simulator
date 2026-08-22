# anpr_sumulator

anpr-camera-simulator/
├── configs/
│   ├── cameras/
│   │   └── satatya_cibr20mvl12cwp_p2.yaml
│   └── scenarios/
│       └── scenario_001.yaml
│
├── src/
│   └── anpr_simulator/
│       ├── camera/
│       ├── geometry/
│       ├── vehicle/
│       ├── plate/
│       ├── exposure/
│       ├── simulation/
│       └── utils/
│
├── tests/
│   ├── test_fov.py
│   ├── test_projection.py
│   ├── test_motion.py
│   ├── test_motion_blur.py
│   └── test_simulation.py
│
├── notebooks/
├── results/
├── tools/
│   └── run_simulation.py
├── pyproject.toml
├── requirements.txt
├── README.md
└── .gitignore

                  Camera
                    │
            CameraPose
          ┌─────────┴─────────┐
          │                   │
       Height               Pitch
          │                   │
          └─────────┬─────────┘
                    │
                    ▼
                  Road
                    │
                    ▼
              Vehicle
          ┌─────────┴─────────┐
          │                   │
      Dimensions          Trajectory
          │                   │
          └─────────┬─────────┘
                    │
                    ▼
             VehicleState
                    │
                    ▼
              WorldPoint
                    │
                    ▼
           World → Camera
                    │
                    ▼
                Point3D
                    │
                    ▼
             Projection
                    │
                    ▼
                Point2D


M1 ── Empty 4K scene
 │
 ▼
M2 ── Moving rectangle vehicle
 │
 ▼
M3 ── License plate rectangle
 │
 ▼
M4 ── Plate follows vehicle
 │
 ▼
M5 ── Plate scaling
 │
 ▼
M6 ── Plate perspective
 │
 ▼
M7 ── Real vehicle image
 │
 ▼
M8 ── Vehicle perspective
 │
 ▼
M9 ── Complete frame sequence
 │
 ▼
M10 ─ Video generation
 │
 ▼
M11 ─ Motion blur
 │
 ▼
M12 ─ Sensor effects