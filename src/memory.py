import json
import datetime as dt
from pathlib import Path
from typing import Any, Dict, Optional, List
from src.logging import get_logger


class Memory:
    """
    Simple JSON‑backed persistent store for user preferences, interactions, and learned facts.
    """

    def __init__(self, path: Path, max_interactions: int = 100) -> None:
        """
        Initialize the memory store.
        Args:
            path (Path): Path to the memory file.
            max_interactions (int): Maximum number of interactions to keep in memory.
        """
        self.path = path
        self.max_interactions = max_interactions
        self.data: Dict[str, Any] = self._load()
        self.logger = get_logger(__name__)

    def _load(self) -> Dict[str, Any]:
        """
        Load memory from disk, or initialize if missing/corrupted.
        Returns:
            Dict[str, Any]: The loaded or default memory structure.
        """
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
            "todo_tasks": [],
            "first_meeting": dt.datetime.now().isoformat(),
        }

    def save(self) -> None:
        """
        Persist memory to disk atomically.
        """
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps(self.data, indent=2), encoding="utf-8")
        tmp.replace(self.path)

    def append(
        self,
        interaction_type: str,
        content: str,
        user_input: Optional[str] = None,
    ) -> None:
        """
        Append an interaction to memory and persist.
        Args:
            interaction_type (str): The type of interaction (e.g., 'user_command', 'ai_response').
            content (str): The content of the interaction.
            user_input (Optional[str]): The original user input, if any.
        """
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

    def add_reminder(self, text: str, when: dt.datetime) -> None:
        """Store a reminder in memory."""
        self.data.setdefault("reminders", []).append(
            {
                "id": dt.datetime.now().isoformat(),
                "text": text,
                "time": when.isoformat(),
            }
        )
        self.save()

    def pop_due_reminders(self, now: Optional[dt.datetime] = None) -> List[Dict[str, Any]]:
        """Return and remove reminders that are due."""
        now = now or dt.datetime.now()
        due = []
        remaining = []
        for rem in self.data.get("reminders", []):
            try:
                rem_time = dt.datetime.fromisoformat(rem.get("time"))
            except Exception:
                rem_time = now
            if rem_time <= now:
                due.append(rem)
            else:
                remaining.append(rem)
        if due:
            self.data["reminders"] = remaining
            self.save()
        return due

    def add_todo(self, text: str) -> None:
        """Add a todo task."""
        self.data.setdefault("todo_tasks", []).append(
            {
                "id": dt.datetime.now().isoformat(),
                "text": text,
                "done": False,
            }
        )
        self.save()

    def list_todo(self) -> List[str]:
        """Return a list of incomplete todo task texts."""
        return [t["text"] for t in self.data.get("todo_tasks", []) if not t.get("done")]

    def complete_todo(self, text: str) -> bool:
        """Mark a todo task as completed."""
        for task in self.data.get("todo_tasks", []):
            if task["text"].lower() == text.lower() and not task.get("done"):
                task["done"] = True
                self.save()
                return True
        return False
