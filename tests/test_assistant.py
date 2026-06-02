from __future__ import annotations

import unittest

from assistant import VoiceAssistant
from commands.base import Command, CommandResult
from speech import ConsoleSTT, ConsoleTTS


class TestSTT(ConsoleSTT):
    def __init__(self, responses: list[str | None] | None = None) -> None:
        super().__init__()
        self.responses = responses or []
        self.index = 0

    def listen(self, timeout: float | None = None) -> str | None:
        if self.index >= len(self.responses):
            return None
        val = self.responses[self.index]
        self.index += 1
        return val


class TestTTS(ConsoleTTS):
    def __init__(self) -> None:
        super().__init__()
        self.spoken: list[str] = []

    def speak(self, text: str) -> None:
        self.spoken.append(text)


class TestCommand(Command):
    name = "test"
    description = "A test command"
    keywords = ["test", "testing"]

    def can_handle(self, text: str) -> float:
        return 1.0 if "test" in text.lower() else 0.0

    def execute(self, text: str) -> CommandResult:
        return CommandResult(success=True, message="Test command executed")


class TestVoiceAssistant(unittest.TestCase):

    def test_hello_greeting(self) -> None:
        assistant = VoiceAssistant()
        result = assistant.process("hello")
        self.assertTrue(result.success)
        self.assertIn("Hello", result.message)

    def test_goodbye_farewell(self) -> None:
        assistant = VoiceAssistant()
        result = assistant.process("goodbye")
        self.assertTrue(result.success)
        self.assertIn("Goodbye", result.message)

    def test_thanks(self) -> None:
        assistant = VoiceAssistant()
        result = assistant.process("thank you")
        self.assertTrue(result.success)
        self.assertIn("welcome", result.message.lower())

    def test_time_command(self) -> None:
        assistant = VoiceAssistant()
        result = assistant.process("what time is it")
        self.assertTrue(result.success)
        self.assertIn("time", result.message.lower())

    def test_help_command(self) -> None:
        assistant = VoiceAssistant()
        result = assistant.process("help me")
        self.assertTrue(result.success)
        self.assertIn("Available commands", result.message)

    def test_exit_command(self) -> None:
        assistant = VoiceAssistant()
        result = assistant.process("exit")
        self.assertTrue(result.success)
        self.assertTrue(result.should_exit)

    def test_unknown_command(self) -> None:
        assistant = VoiceAssistant()
        result = assistant.process("xyzzy this is gibberish")
        self.assertFalse(result.success)
        self.assertIn("sorry", result.message.lower())

    def test_register_custom_command(self) -> None:
        assistant = VoiceAssistant()
        cmd = TestCommand()
        assistant.register_command(cmd)
        result = assistant.process("run the test please")
        self.assertTrue(result.success)
        self.assertEqual(result.message, "Test command executed")

    def test_empty_input(self) -> None:
        assistant = VoiceAssistant()
        result = assistant.process("")
        self.assertTrue(result.success)
        self.assertEqual(result.message, "")

    def test_run_once_exit(self) -> None:
        stt = TestSTT(responses=["exit"])
        tts = TestTTS()
        assistant = VoiceAssistant(stt=stt, tts=tts)
        result = assistant.run_once()
        self.assertFalse(result)
        self.assertEqual(tts.spoken[-1], "Goodbye!")

    def test_intent_classification(self) -> None:
        from intents import IntentClassifier
        classifier = IntentClassifier()
        self.assertEqual(classifier.classify("hello there"), "greeting")
        self.assertEqual(classifier.classify("bye"), "farewell")
        self.assertEqual(classifier.classify("thanks a lot"), "thanks")
        self.assertEqual(classifier.classify("what is the time"), "command")


if __name__ == "__main__":
    unittest.main()
