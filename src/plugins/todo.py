from __future__ import annotations
import re
from src.plugins.base import AssistantPlugin


class TodoPlugin(AssistantPlugin):
    """Simple todo list management plugin."""

    name = "Todo"
    description = "Manage a personal todo list."

    def setup(self, assistant) -> None:
        self.memory = assistant.memory

    def register(self):
        return {"todo": self.handle_todo}

    def handle_todo(self, command: str, *args, **kwargs):
        cmd = command.lower()
        add_match = re.search(r"add (.+?) to(?: my)? todo list", cmd)
        if add_match:
            task = add_match.group(1).strip()
            self.memory.add_todo(task)
            return f"Added '{task}' to your todo list."

        if any(word in cmd for word in ("list", "show", "what")):
            tasks = self.memory.list_todo()
            if not tasks:
                return "Your todo list is empty."
            numbered = [f"{i + 1}. {t}" for i, t in enumerate(tasks)]
            return "Here is your todo list:\n" + "\n".join(numbered)

        done_match = re.search(
            r"(?:mark|complete|finish|remove) (.+?) (?:from .*|as done)?", cmd
        )
        if done_match:
            task = done_match.group(1).strip()
            if self.memory.complete_todo(task):
                return f"Marked '{task}' as done."
            return f"I couldn't find '{task}' on your todo list."

        return (
            "To manage your todo list, say something like 'add buy milk to my todo "
            "list' or 'list my todo list'."
        )
