"""Short on-screen messages shown in the message bar at the bottom of the grid.

Call notify("text") from anywhere; hud.draw_message_bar() renders it and
fades it out after MESSAGE_DURATION_MS. A new message replaces the old one.
"""

import pygame

from .config import MESSAGE_DURATION_MS, MESSAGE_FADE_MS

_text = None
_started_ms = 0


def notify(text):
    global _text, _started_ms
    _text = text
    _started_ms = pygame.time.get_ticks()


def clear():
    global _text
    _text = None


def current():
    """Return (text, alpha 0-255) for the active message, or None if there isn't one."""
    global _text
    if _text is None:
        return None
    elapsed = pygame.time.get_ticks() - _started_ms
    if elapsed >= MESSAGE_DURATION_MS:
        _text = None
        return None
    fade_start = MESSAGE_DURATION_MS - MESSAGE_FADE_MS
    if elapsed <= fade_start:
        alpha = 255
    else:
        alpha = int(255 * (MESSAGE_DURATION_MS - elapsed) / MESSAGE_FADE_MS)
    return _text, alpha
