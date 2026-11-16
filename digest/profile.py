"""The user profile: what they care about, and where/when to deliver the digest."""

from dataclasses import asdict, dataclass, field
from pathlib import Path

import yaml

CONFIG_PATH = Path("config.yaml")


@dataclass
class Interest:
    name: str
    tags: list[str] = field(default_factory=list)


@dataclass
class Profile:
    email: str
    send_time: str  # "HH:MM", 24-hour local time
    interests: list[Interest] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Profile":
        return cls(
            email=str(data["email"]),
            send_time=str(data["send_time"]),
            interests=[Interest(**i) for i in data.get("interests", [])],  # type: ignore[arg-type]
        )

    def save(self, path: Path) -> None:
        path.write_text(yaml.safe_dump(self.to_dict(), sort_keys=False), encoding="utf-8")

    @classmethod
    def load(cls, path: Path = CONFIG_PATH) -> "Profile":
        return cls.from_dict(yaml.safe_load(path.read_text(encoding="utf-8")))
