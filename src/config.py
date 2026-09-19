from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    token: str
    guild_id: int | None
    feed_url: str | None
    poll_seconds: int
    timeout_seconds: int

def load_settings() -> Settings:
    token = os.getenv("DISCORD_TOKEN", "").strip()
    if not token:
        raise RuntimeError("DISCORD_TOKEN is required")
    guild = os.getenv("DISCORD_GUILD_ID", "").strip()
    return Settings(
        token=token,
        guild_id=int(guild) if guild else None,
        feed_url=os.getenv("POKEMON_FEED_URL", "").strip() or None,
        poll_seconds=max(30, int(os.getenv("POLL_SECONDS", "60"))),
        timeout_seconds=max(3, int(os.getenv("HTTP_TIMEOUT_SECONDS", "12"))),
    )
