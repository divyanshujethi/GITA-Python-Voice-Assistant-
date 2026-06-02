from __future__ import annotations

import logging
import re

logger = logging.getLogger(__name__)

GREETING_PATTERNS = [
    re.compile(r"\b(hello|hi|hey|good morning|good afternoon|good evening)\b", re.IGNORECASE),
]
FAREWELL_PATTERNS = [
    re.compile(r"\b(bye|goodbye|see you|exit|quit)\b", re.IGNORECASE),
]
THANKS_PATTERNS = [
    re.compile(r"\b(thanks|thank you|appreciate it)\b", re.IGNORECASE),
]


class IntentClassifier:
    def classify(self, text: str) -> str:
        lower = text.lower().strip()
        for pat in GREETING_PATTERNS:
            if pat.search(lower):
                return "greeting"
        for pat in FAREWELL_PATTERNS:
            if pat.search(lower):
                return "farewell"
        for pat in THANKS_PATTERNS:
            if pat.search(lower):
                return "thanks"
        if len(lower) < 3:
            return "unknown"
        return "command"
