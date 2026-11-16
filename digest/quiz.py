"""Interactive onboarding: pick interests, answer follow-ups, set email and send time."""

import re

from digest.interests import CATALOG
from digest.profile import CONFIG_PATH, Interest, Profile

_TIME_RE = re.compile(r"^([01]\d|2[0-3]):[0-5]\d$")


def _pick(prompt: str, options: list[str], allow_all: bool = False) -> list[str]:
    for i, opt in enumerate(options, 1):
        print(f"  {i}. {opt}")
    raw = input(f"{prompt} ").strip()
    if not raw and allow_all:
        return options.copy()
    picks: list[str] = []
    for token in raw.split(","):
        idx = int(token.strip()) - 1
        if not 0 <= idx < len(options):
            raise SystemExit(f"Invalid selection: {token.strip()!r} (1-{len(options)})")
        picks.append(options[idx])
    return picks


def run_setup() -> None:
    print("Let's build your digest profile.\n")
    names = _pick("Pick your interests (e.g. 1,3,7):", list(CATALOG))
    interests: list[Interest] = []
    for name in names:
        tags = _pick(f"Topics for {name} (blank = all):", CATALOG[name], allow_all=True)
        interests.append(Interest(name=name, tags=tags))
        print()
    email = input("Email to send your digest to: ").strip()
    send_time = input("Daily send time (HH:MM, 24h): ").strip()
    if not _TIME_RE.match(send_time):
        raise SystemExit(f"Invalid time {send_time!r} — use HH:MM, e.g. 07:30")
    Profile(email=email, send_time=send_time, interests=interests).save(CONFIG_PATH)
    print(f"\nSaved to {CONFIG_PATH}. Run `digest send` for your first digest.")
