import json
from pathlib import Path
from typing import Any, Dict
from src.logging import get_logger


class Memory:
    """Simple JSON‑backed persistent store."""

    def __init__(self, path: Path, max_interactions: int = 100) -> None:
        self.path = path
        self.max_interactions = max_interactions
        self.data: Dict[str, Any] = self._load()
        self.logger = get_logger(__name__)

    def _load(self) -> Dict[str, Any]:
        if self.path.exists():
            try:
                with self.path.open("r", encoding="utf-8") as fh:
                    return json.load(fh)
            except json.JSONDecodeError:
                self.logger.warning("Memory file corrupted – starting fresh.")
        return {
            "user_preferences": {},
            "interactions": [],
            "learned_facts": {},
            "reminders": [],
            "first_meeting": dt.datetime.now().isoformat(),
        }

    def save(self) -> None:
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps(self.data, indent=2), encoding="utf-8")
        tmp.replace(self.path)

    def append(
        self,
        interaction_type: str,
        content: str,
        user_input: str | None = None,
    ) -> None:
        self.data.setdefault("interactions", []).append(
            {
                "timestamp": dt.datetime.now().isoformat(),
                "type": interaction_type,
                "content": content,
                "user_input": user_input,
            }
        )
        if len(self.data["interactions"]) > self.max_interactions:
            self.data["interactions"] = self.data["interactions"][-self.max_interactions:]
        self.save() 