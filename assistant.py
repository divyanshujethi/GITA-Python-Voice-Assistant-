from __future__ import annotations

import logging

from commands import CommandRegistry, CommandResult
from commands.exit_command import ExitCommand
from commands.help_command import HelpCommand
from commands.time_command import TimeCommand
from intents import IntentClassifier
from speech import ConsoleTTS, ConsoleSTT, STTEngine, TTSEngine

logger = logging.getLogger(__name__)


class VoiceAssistant:
    def __init__(
        self,
        name: str = "Assistant",
        stt: STTEngine | None = None,
        tts: TTSEngine | None = None,
    ) -> None:
        self.name = name
        self.stt = stt or ConsoleSTT()
        self.tts = tts or ConsoleTTS()
        self.intent_classifier = IntentClassifier()
        self.command_registry = CommandRegistry()
        self.running = False

        self._register_default_commands()

    def _register_default_commands(self) -> None:
        self.command_registry.register(TimeCommand())
        help_cmd = HelpCommand(self.command_registry)
        self.command_registry.register(help_cmd)
        self.command_registry.register(ExitCommand())

    def register_command(self, command) -> None:
        self.command_registry.register(command)

    def _handle_intent(self, text: str) -> str | None:
        intent = self.intent_classifier.classify(text)
        if intent == "greeting":
            return f"Hello! How can I help you?"
        if intent == "farewell":
            return "Goodbye!"
        if intent == "thanks":
            return "You're welcome!"
        return None

    def process(self, text: str) -> CommandResult:
        if not text:
            return CommandResult(success=True)

        cmd = self.command_registry.get_best_match(text)
        if cmd is not None:
            return cmd.execute(text)

        response = self._handle_intent(text)
        if response:
            return CommandResult(success=True, message=response)

        return CommandResult(
            success=False,
            message=f"Sorry, I don't know how to handle that. Say 'help' to see available commands.",
        )

    def run_once(self) -> bool:
        text = self.stt.listen()
        if text is None:
            return True

        result = self.process(text)

        if result.message:
            self.tts.speak(result.message)

        if result.should_exit:
            self.running = False
            return False
        return True

    def run(self) -> None:
        self.running = True
        self.tts.speak(f"{self.name} ready. How can I help you?")
        try:
            while self.running:
                if not self.run_once():
                    break
        except KeyboardInterrupt:
            self.tts.speak("Shutting down.")
