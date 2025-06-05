from dataclasses import dataclass, field
import os
from pathlib import Path
from typing import List


@dataclass
class Settings:
    """Runtime configuration pulled from env vars with sane defaults."""
    api_key: str = field(
        default_factory=lambda: os.getenv("ELEVENLABS_API_KEY", "")
    )
    openai_api_key: str = field(
        default_factory=lambda: os.getenv("OPENAI_API_KEY", "")
    )
    openai_model_name: str = os.getenv(
        "OPENAI_MODEL_NAME", "gpt-3.5-turbo"
    )
    voice_id: str = (
        "AwbZ3Leiit6t97L6NM4u"
    )  # public demo voice – change as desired
    memory_path: Path = Path("./ai_memory.json")
    wake_words: List[str] = field(
        default_factory=lambda: [
            "hey assistant",
            "hello assistant",
            "assistant",
        ]
    )
    max_interactions: int = 100
    ambient_adjust_sec: float = 0.5
    listen_timeout: int = 10
    phrase_time_limit: int = 7

    @property
    def tts_url(self) -> str:
        return (
            f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}"
        ) 