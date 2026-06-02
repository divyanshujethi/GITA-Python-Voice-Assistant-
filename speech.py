from __future__ import annotations

import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class STTEngine(ABC):
    @abstractmethod
    def listen(self, timeout: float | None = None) -> str | None:
        ...


class TTSEngine(ABC):
    @abstractmethod
    def speak(self, text: str) -> None:
        ...


class SpeechRecognitionSTT(STTEngine):
    def __init__(self) -> None:
        try:
            import speech_recognition as sr
            self._recognizer = sr.Recognizer()
            self._microphone = sr.Microphone()
            self._ready = True
        except ImportError:
            logger.warning("SpeechRecognition not installed; STT disabled")
            self._ready = False

    def listen(self, timeout: float | None = 5.0) -> str | None:
        if not self._ready:
            return None
        import speech_recognition as sr
        with self._microphone as source:
            self._recognizer.adjust_for_ambient_noise(source, duration=0.5)
            logger.info("Listening...")
            try:
                audio = self._recognizer.listen(source, timeout=timeout)
            except sr.WaitTimeoutError:
                return None
        try:
            text = self._recognizer.recognize_google(audio)
            logger.info("Heard: %s", text)
            return text
        except (sr.UnknownValueError, sr.RequestError):
            return None


class Pyttsx3TTS(TTSEngine):
    def __init__(self) -> None:
        try:
            import pyttsx3
            self._engine = pyttsx3.init()
            self._ready = True
        except ImportError:
            logger.warning("pyttsx3 not installed; TTS disabled")
            self._ready = False

    def speak(self, text: str) -> None:
        if not self._ready:
            logger.info("TTS: %s", text)
            return
        self._engine.say(text)
        self._engine.runAndWait()


class ConsoleSTT(STTEngine):
    def listen(self, timeout: float | None = None) -> str | None:
        try:
            return input("You: ").strip() or None
        except (EOFError, KeyboardInterrupt):
            return None


class ConsoleTTS(TTSEngine):
    def speak(self, text: str) -> None:
        print(f"Assistant: {text}")
