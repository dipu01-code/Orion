"""Environment-only runtime configuration. Secrets are never logged."""

from dataclasses import dataclass
import os
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    provider: str | None
    api_key: str | None
    model: str | None
    base_url: str
    database_path: Path
    system_instruction: str

    @classmethod
    def from_environment(cls) -> "Settings":
        return cls(
            provider=os.getenv("ORION_MODEL_PROVIDER"),
            api_key=os.getenv("OPENAI_API_KEY"),
            model=os.getenv("OPENAI_MODEL"),
            base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
            database_path=Path(os.getenv("ORION_MEMORY_DB", "orion_memory.sqlite3")),
            system_instruction=os.getenv(
                "ORION_SYSTEM_INSTRUCTION",
                "You are ORION, a helpful, concise, and safety-conscious desktop assistant.",
            ),
        )
