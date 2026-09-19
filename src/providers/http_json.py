import aiohttp
from ..models import Spawn

class HttpJsonProvider:
    def __init__(self, url: str | None, timeout: int = 12):
        self.url = url
        self.timeout = aiohttp.ClientTimeout(total=timeout)

    async def fetch(self) -> list[Spawn]:
        if not self.url:
            return []
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            async with session.get(self.url, headers={"User-Agent": "PokeHunter/1.0"}) as r:
                r.raise_for_status()
                payload = await r.json(content_type=None)
        rows = payload.get("pokemon", payload.get("spawns", payload.get("data", payload))) if isinstance(payload, dict) else payload
        if not isinstance(rows, list):
            return []
        out = []
        for row in rows:
            if isinstance(row, dict):
                try:
                    out.append(Spawn.from_mapping(row))
                except (ValueError, TypeError):
                    pass
        return out
