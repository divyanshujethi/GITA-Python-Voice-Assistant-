# GITA — Voice Assistant

A Python-based voice assistant that runs entirely on your local machine. GITA supports both text and voice input modes, intent classification, and an extensible command system — no cloud, no API keys.

## Overview

GITA is a modular, offline-first voice assistant built with Python. It listens for your commands via microphone (or console input), classifies intent using regex patterns, dispatches to registered commands, and speaks responses back to you.

### Architecture

```
code/
├── main.py              # Entry point — CLI argument parsing and mode selection
├── assistant.py         # VoiceAssistant: orchestration, intent handling, command dispatch
├── speech.py            # STT/TTS engines (SpeechRecognition, pyttsx3, console fallbacks)
├── intents.py           # IntentClassifier — regex-based greeting/farewell/thanks detection
├── commands/
│   ├── base.py          # Command, CommandResult, CommandRegistry ABCs
│   ├── help_command.py  # Lists available commands
│   ├── time_command.py  # Reports current date and time
│   └── exit_command.py  # Gracefully shuts down the assistant
├── tests/
│   └── test_assistant.py
└── requirements.txt
```

### Features

| Feature                     | Description                                          |
| --------------------------- | ---------------------------------------------------- |
| **Text mode**               | Typed input, console output — no audio hardware needed |
| **Voice mode**              | Microphone input, spoken output — requires audio stack |
| **Intent classification**   | Detects greetings, farewells, and thanks via regex   |
| **Command registry**        | Extensible plugin-like system for adding new commands |
| **Built-in commands**       | `time`, `help`, `exit`                               |
| **100% local**              | No cloud dependencies, no data leaves your machine   |
| **Graceful fallbacks**      | Works even when audio libraries are missing          |

## Prerequisites

### Hardware

- **Microphone** (required for voice mode only)
- **Speakers or headphones** (required for voice mode only)

### Software (Fedora)

- **Python**: 3.10 or later
- **pip**: Python package manager
- **PortAudio**: Audio I/O library (required for `pyaudio` in voice mode)
- **ALSA / PulseAudio**: Linux audio system (pre-installed on Fedora)

## Installation

### 1. Install System Dependencies (Fedora)

```bash
sudo dnf install -y python3 python3-pip python3-devel portaudio-devel pulseaudio-libs-devel
```

Verify the installation:

```bash
python3 --version   # Expected: Python 3.10 or later
pip3 --version      # Expected: pip 23.x or later
```

### 2. Clone the Repository

```bash
git clone <repository-url>
cd voice-assistant-python
```

### 3. Create a Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate
```

Your prompt will change to show `(venv)`.

### 4. Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r code/requirements.txt
```

**Expected output:**

```
Successfully installed SpeechRecognition-3.10.0 pyttsx3-2.90 pyaudio-0.2.11 ...
```

### 5. Install Test Dependencies (Optional)

```bash
pip install pytest
```

## Usage

### Text Mode (Default)

No audio hardware required. Type commands, see responses on screen.

```bash
cd code
python main.py
```

**Example session:**

```
Assistant: GITA ready. How can I help you?
You: hello
Assistant: Hello! How can I help you?
You: what time is it
Assistant: The current date and time is Monday, June 01, 2026 at 02:30 PM.
You: help
Assistant: Available commands:
  time - Tell the current date and time
  help - List all available commands
  exit - Exit the voice assistant
You: exit
Assistant: Goodbye!
```

### Voice Mode

Requires a working microphone and speakers/headphones.

```bash
cd code
python main.py --mode voice
```

GITA will listen through your microphone and respond through speakers. Speak naturally — the assistant recognizes greetings, time queries, and exit commands.

### Verbose Logging

Enable debug output to see what is happening under the hood:

```bash
python main.py --verbose
# or
python main.py --mode voice --verbose
```

### Run Tests

```bash
cd code
pytest tests/ -v
```

**Expected output:**

```
tests/test_assistant.py .............                         [100%]
```

## Configuration

### Command-Line Arguments

| Argument             | Default | Description                          |
| -------------------- | ------- | ------------------------------------ |
| `--mode`             | `text`  | Input mode: `voice` or `text`        |
| `--verbose` / `-v`   | `false` | Enable debug-level logging           |

### Adding Custom Commands

Create a new file in `code/commands/` and subclass `Command`:

```python
from commands.base import Command, CommandResult

class WeatherCommand(Command):
    name = "weather"
    description = "Get the current weather"
    keywords = ["weather", "forecast", "temperature"]

    def can_handle(self, text: str) -> float:
        return 1.0 if any(kw in text.lower() for kw in self.keywords) else 0.0

    def execute(self, text: str) -> CommandResult:
        return CommandResult(success=True, message="The weather is sunny and 72°F.")
```

Then register it in `main.py`:

```python
from commands import WeatherCommand
assistant.register_command(WeatherCommand())
```

### Intent Configuration

Edit `code/intents.py` to add or modify intent patterns. The classifier uses regex:

```python
GREETING_PATTERNS = [
    re.compile(r"\b(hello|hi|hey|good morning|good afternoon|good evening)\b", re.IGNORECASE),
]
```

## Troubleshooting

### `pip install` fails on building `pyaudio`

**Problem**: PortAudio development headers are missing.

**Solution**:

```bash
sudo dnf install -y portaudio-devel pulseaudio-libs-devel
pip install --force-reinstall pyaudio
```

### Voice mode: "STT disabled" / "TTS disabled" warning

**Problem**: Required audio libraries are not installed.

**Solution**:

```bash
pip install SpeechRecognition pyttsx3 pyaudio
```

### Microphone not detected

**Problem**: `SpeechRecognition` cannot find a microphone.

**Solution** — list available microphones:

```bash
python3 -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_names())"
```

If the list is empty, ensure PulseAudio is running:

```bash
pulseaudio --start
```

### `No module named 'commands'`

**Problem**: The script is not being run from the `code/` directory.

**Solution**:

```bash
cd code
python main.py
```

### Permission denied for microphone (Fedora)

**Problem**: The system blocks microphone access.

**Solution** — install and configure ALSA/PulseAudio:

```bash
sudo dnf install -y pulseaudio-utils alsa-utils
pulseaudio --start
```

Grant microphone access in Fedora's privacy settings if using a desktop environment.

### Tests fail with module import errors

**Problem**: pytest cannot find project modules.

**Solution**:

```bash
cd code
pip install -e .
pytest tests/ -v
```

## Project Roadmap

- [x] Intent classification (greetings, farewells, thanks)
- [x] Command registry with time, help, exit
- [x] Text mode (console I/O)
- [x] Voice mode (via SpeechRecognition + pyttsx3)
- [x] Unit tests
- [ ] Web search command
- [ ] Reminder / alarm system
- [ ] LLM integration for open-domain Q&A
