from readme.svg.showcase import SvgShowcase


def test_shot_is_inset_and_runs_off_the_bottom() -> None:
    shot = SvgShowcase.shot(width=400, height=320, ratio=1.25)

    assert shot.x == SvgShowcase.INSET_X
    assert shot.y == SvgShowcase.INSET_Y
    assert shot.width == 400 - 2 * SvgShowcase.INSET_X
    assert shot.y + shot.height > 320


def test_wide_shots_keep_their_ratio() -> None:
    shot = SvgShowcase.shot(width=490, height=250, ratio=1.6)

    assert shot.height == shot.width / 1.6
