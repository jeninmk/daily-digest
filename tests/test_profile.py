from pathlib import Path

from digest.profile import Interest, Profile


def test_round_trip(tmp_path: Path) -> None:
    profile = Profile(
        email="a@b.c",
        send_time="07:00",
        interests=[Interest(name="tech", tags=["AI"])],
    )
    path = tmp_path / "config.yaml"
    profile.save(path)
    assert Profile.load(path) == profile
