from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class CommandResult:
    success: bool
    message: str = ""
    data: dict[str, Any] | None = None
    should_exit: bool = False

    def __bool__(self) -> bool:
        return self.success


class Command(ABC):
    name: str = ""
    description: str = ""
    keywords: list[str] = field(default_factory=list)

    @abstractmethod
    def can_handle(self, text: str) -> float:
        ...

    @abstractmethod
    def execute(self, text: str) -> CommandResult:
        ...


class CommandRegistry:
    def __init__(self) -> None:
        self._commands: dict[str, Command] = {}

    def register(self, command: Command) -> None:
        self._commands[command.name] = command

    def get_best_match(self, text: str) -> Command | None:
        best_score = 0.0
        best_cmd: Command | None = None
        for cmd in self._commands.values():
            score = cmd.can_handle(text)
            if score > best_score:
                best_score = score
                best_cmd = cmd
        return best_cmd

    def all_commands(self) -> list[Command]:
        return list(self._commands.values())

    def get(self, name: str) -> Command | None:
        return self._commands.get(name)
