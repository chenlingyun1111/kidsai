import re

BLOCKED_PATTERNS = [
    r"\b(kill|die|dead|murder|weapon|gun|knife)\b",
    r"\b(sex|nude|naked|porn)\b",
    r"\b(drug|cocaine|marijuana)\b",
    r"\b(suicide|self.harm)\b",
]

_compiled = [re.compile(p, re.IGNORECASE) for p in BLOCKED_PATTERNS]


def is_safe(text: str) -> bool:
    return not any(p.search(text) for p in _compiled)


def sanitize_output(text: str, redirect_message: str = "Let's talk about something fun instead!") -> str:
    if is_safe(text):
        return text
    return redirect_message
