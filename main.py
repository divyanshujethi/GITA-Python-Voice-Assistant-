from __future__ import annotations

import argparse
import logging
import sys

from assistant import VoiceAssistant
from speech import ConsoleSTT, ConsoleTTS, SpeechRecognitionSTT, Pyttsx3TTS


def setup_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.WARNING
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Voice Assistant")
    parser.add_argument(
        "--mode",
        choices=["voice", "text"],
        default="text",
        help="Input mode: voice (mic) or text (console)",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable debug logging")
    args = parser.parse_args()

    setup_logging(args.verbose)

    if args.mode == "voice":
        stt: ConsoleSTT | SpeechRecognitionSTT = SpeechRecognitionSTT()
        tts: ConsoleTTS | Pyttsx3TTS = Pyttsx3TTS()
    else:
        stt = ConsoleSTT()
        tts = ConsoleTTS()

    assistant = VoiceAssistant(name="GITA", stt=stt, tts=tts)

    try:
        assistant.run()
    except KeyboardInterrupt:
        print()
        sys.exit(0)


if __name__ == "__main__":
    main()
