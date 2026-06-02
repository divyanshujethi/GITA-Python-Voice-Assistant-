from __future__ import annotations

from datetime import datetime

from .base import Command, CommandResult


class TimeCommand(Command):
    name = "time"
    description = "Tell the current date and time"
    keywords = ["time", "date", "what time", "what's the time", "today", "current time"]

    def can_handle(self, text: str) -> float:
        lower = text.lower()
        for kw in self.keywords:
            if kw in lower:
                return 1.0
        return 0.0

    def execute(self, text: str) -> CommandResult:
        now = datetime.now()
        formatted = now.strftime("%A, %B %d, %Y at %I:%M %p")
        return CommandResult(success=True, message=f"The current date and time is {formatted}.")
