from generate_anpr_sequence import build_generator, build_parser


def test_cli_defaults_create_visible_late_plate():
    args = build_parser().parse_args([])
    generator = build_generator(args)
    frame = next(generator.generate())

    assert args.camera_height_m == 2.0
    assert args.initial_distance_m == 30.0
    assert args.fx == 2500.0
    assert frame.projected_plate.width_pixels > 35.0
