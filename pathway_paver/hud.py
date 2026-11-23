"""Header bar (level name, tile/turn counters, buttons) and the message bar."""

import pygame

from . import notifications, state
from .config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, HEADER_HEIGHT, HEADER_BG, HEADER_DIVIDER,
    BLACK, WHITE, WARNING, MESSAGE_BG, FONT_HEADER, FONT_MESSAGE,
    LOW_TURNS_THRESHOLD,
)
from .display import screen
from .levels import levels

HEADER_PADDING_X = 12
HEADER_SECTION_GAP = 28  # Space between header sections (divider sits in the middle)

READY_HINT = "All cars connected. Press SPACE to start."


def draw_header():
    header_rect = pygame.Rect(0, 0, SCREEN_WIDTH, HEADER_HEIGHT)
    pygame.draw.rect(screen, HEADER_BG, header_rect)

    level = levels[state.currentLevel]
    font = pygame.font.Font(None, FONT_HEADER)

    tiles_color = WARNING if state.current_tile_count >= level["max_tiles"] else BLACK
    turns_shown = max(state.turns_left, 0)
    turns_color = WARNING if turns_shown <= LOW_TURNS_THRESHOLD else BLACK

    sections = [
        (level["name"], BLACK),
        (f"Tiles {state.current_tile_count}/{level['max_tiles']}", tiles_color),
        (f"Turns {turns_shown}/{level['max_turns']}", turns_color),
    ]

    # Lay out sections left to right, vertically centered, with dividers between them
    x = HEADER_PADDING_X
    center_y = HEADER_HEIGHT // 2
    for i, (text, color) in enumerate(sections):
        if i > 0:
            divider_x = x - HEADER_SECTION_GAP // 2
            pygame.draw.line(screen, HEADER_DIVIDER, (divider_x, 12), (divider_x, HEADER_HEIGHT - 12), 1)
        surface = font.render(text, True, color)
        screen.blit(surface, surface.get_rect(midleft=(x, center_y)))
        x += surface.get_width() + HEADER_SECTION_GAP

    for btn in state.header_buttons:
        btn.draw(screen)


def draw_message_bar():
    """Show the active message, or the 'ready' hint while planning a fully connected level."""
    active = notifications.current()
    if active is not None:
        text, alpha = active
    elif not state.move_mode and state.game_outcome is None and state.all_connected:
        text, alpha = READY_HINT, 255
    else:
        return

    font = pygame.font.Font(None, FONT_MESSAGE)
    text_surface = font.render(text, True, WHITE)
    box = text_surface.get_rect().inflate(32, 16)
    box.midbottom = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 12)

    bar = pygame.Surface(box.size, pygame.SRCALPHA)
    pygame.draw.rect(bar, (*MESSAGE_BG, int(alpha * 0.85)), bar.get_rect(), border_radius=10)
    text_surface.set_alpha(alpha)
    bar.blit(text_surface, text_surface.get_rect(center=bar.get_rect().center))
    screen.blit(bar, box)
