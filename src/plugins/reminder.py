from __future__ import annotations
import re
import dateparser
from src.plugins.base import AssistantPlugin

class ReminderPlugin(AssistantPlugin):
    name = "Reminder"
    description = "Set and announce time-based reminders."

    def setup(self, assistant) -> None:
        self.memory = assistant.memory

    def register(self):
        return {"remind": self.handle_reminder}

    def handle_reminder(self, command: str, *args, **kwargs):
        match = re.search(r"remind(?: me)? to (.+?) at (.+)", command, re.IGNORECASE)
        if not match:
            return "Please specify a reminder like 'remind me to buy milk at 6pm'."
        task, time_str = match.groups()
        when = dateparser.parse(time_str)
        if not when:
            return f"I couldn't understand the time '{time_str}'."
        self.memory.add_reminder(task.strip(), when)
        return f"Okay, I'll remind you to {task.strip()} at {when.strftime('%I:%M %p on %B %d')}"
