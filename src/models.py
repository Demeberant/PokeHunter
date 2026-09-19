from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class Spawn:
    id: str
    pokemon: str
    latitude: float
    longitude: float
    iv: float | None = None
    level: float | None = None
    cp: int | None = None
    size: str | None = None
    expires_at: str | None = None

    @classmethod
    def from_mapping(cls, x: dict[str, Any]) -> "Spawn":
        name = x.get("pokemon") or x.get("name") or x.get("pokemon_name")
        lat = x.get("latitude", x.get("lat"))
        lon = x.get("longitude", x.get("lng", x.get("lon")))
        if name is None or lat is None or lon is None:
            raise ValueError("missing pokemon/coordinates")
        sid = str(x.get("id") or x.get("encounter_id") or f"{name}:{lat}:{lon}")
        size = x.get("size") or x.get("size_class")
        return cls(
            id=sid,
            pokemon=str(name),
            latitude=float(lat),
            longitude=float(lon),
            iv=float(x["iv"]) if x.get("iv") is not None else None,
            level=float(x["level"]) if x.get("level") is not None else None,
            cp=int(x["cp"]) if x.get("cp") is not None else None,
            size=str(size).upper() if size is not None else None,
            expires_at=str(x.get("expires_at") or x.get("expire_timestamp") or "") or None,
        )
