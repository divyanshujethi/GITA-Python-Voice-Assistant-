from __future__ import annotations

from .base import Command, CommandRegistry, CommandResult


class HelpCommand(Command):
    name = "help"
    description = "List all available commands"
    keywords = ["help", "what can you do", "commands", "options"]

    def __init__(self, registry: CommandRegistry | None = None) -> None:
        self._registry = registry

    def can_handle(self, text: str) -> float:
        lower = text.lower()
        for kw in self.keywords:
            if kw in lower:
                return 1.0
        return 0.0

    def execute(self, text: str) -> CommandResult:
        if self._registry is None:
            return CommandResult(success=True, message="No commands registered.")
        lines = ["Available commands:"]
        for cmd in self._registry.all_commands():
            lines.append(f"  {cmd.name} - {cmd.description}")
        return CommandResult(success=True, message="\n".join(lines))
