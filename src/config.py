from dataclasses import dataclass, field
import os
from pathlib import Path
from typing import List, Optional
import yaml
from dotenv import load_dotenv

try:
    from pydantic import BaseModel, ValidationError
    USE_PYDANTIC = True
except ImportError:
    BaseModel = object
    ValidationError = Exception
    USE_PYDANTIC = False

load_dotenv()

CONFIG_YAML = os.getenv("CONFIG_YAML", "config.yaml")


def _load_yaml_config(path: str) -> dict:
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    return {}


def _env_or_yaml(key: str, yaml_cfg: dict, default=None):
    return os.getenv(key) or yaml_cfg.get(key.lower()) or default


class Settings(BaseModel if USE_PYDANTIC else object):
    """
    Runtime configuration loaded from .env, config.yaml, and environment variables.
    """
    api_key: str = ""
    openai_api_key: str = ""
    openai_model_name: str = "gpt-3.5-turbo"
    voice_id: str = "AwbZ3Leiit6t97L6NM4u"
    memory_path: Path = Path("./ai_memory.json")
    wake_words: List[str] = field(default_factory=lambda: [
        "hey assistant", "hello assistant", "assistant"
    ])
    max_interactions: int = 100
    ambient_adjust_sec: float = 0.5
    listen_timeout: int = 10
    phrase_time_limit: int = 7

    @property
    def tts_url(self) -> str:
        return f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}"

    @classmethod
    def load(cls) -> "Settings":
        yaml_cfg = _load_yaml_config(CONFIG_YAML)
        kwargs = {
            "api_key": _env_or_yaml("ELEVENLABS_API_KEY", yaml_cfg, ""),
            "openai_api_key": _env_or_yaml("OPENAI_API_KEY", yaml_cfg, ""),
            "openai_model_name": _env_or_yaml("OPENAI_MODEL_NAME", yaml_cfg, "gpt-3.5-turbo"),
            "voice_id": _env_or_yaml("VOICE_ID", yaml_cfg, "AwbZ3Leiit6t97L6NM4u"),
            "memory_path": Path(_env_or_yaml("MEMORY_PATH", yaml_cfg, "./ai_memory.json")),
            "wake_words": yaml_cfg.get("wake_words") or [
                "hey assistant", "hello assistant", "assistant"
            ],
            "max_interactions": int(_env_or_yaml("MAX_INTERACTIONS", yaml_cfg, 100)),
            "ambient_adjust_sec": float(_env_or_yaml("AMBIENT_ADJUST_SEC", yaml_cfg, 0.5)),
            "listen_timeout": int(_env_or_yaml("LISTEN_TIMEOUT", yaml_cfg, 10)),
            "phrase_time_limit": int(_env_or_yaml("PHRASE_TIME_LIMIT", yaml_cfg, 7)),
        }
        if USE_PYDANTIC:
            try:
                return cls(**kwargs)
            except ValidationError as e:
                raise RuntimeError(f"Config validation error: {e}")
        else:
            s = cls()
            for k, v in kwargs.items():
                setattr(s, k, v)
            return s 