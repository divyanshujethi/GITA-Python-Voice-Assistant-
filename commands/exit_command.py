from __future__ import annotations

from .base import Command, CommandResult


class ExitCommand(Command):
    name = "exit"
    description = "Exit the voice assistant"
    keywords = ["exit", "quit", "goodbye", "bye", "stop", "shutdown"]

    def can_handle(self, text: str) -> float:
        lower = text.lower()
        for kw in self.keywords:
            if kw in lower:
                return 1.0
        return 0.0

    def execute(self, text: str) -> CommandResult:
        return CommandResult(success=True, message="Goodbye!", should_exit=True)
