"""Clickable button widgets and small drawing helpers."""

import pygame

from .config import ACCENT, HOVER, WHITE, BLACK, DISABLED, FONT_BUTTON, BUTTON_PADDING_X


def readable_text_color(background):
    """Black or white, whichever is easier to read on the given background color."""
    r, g, b = background[:3]
    luminance = 0.299 * r + 0.587 * g + 0.114 * b
    return BLACK if luminance > 150 else WHITE


class Button:
    """Standard button. Pass width=None to size it to its text.

    Hover color is applied automatically in draw(), so a button only needs to
    be redrawn each frame. A disabled button is grayed out and ignores clicks.
    """

    font_size = FONT_BUTTON

    def __init__(self, text, x, y, width, height, callback, disabled=False):
        self.text = text
        self.font = pygame.font.Font(None, self.font_size)
        if width is None:
            width = self.font.size(text)[0] + 2 * BUTTON_PADDING_X
        self.rect = pygame.Rect(x, y, width, height)
        self.callback = callback
        self.disabled = disabled
        self.base_color = ACCENT
        self.hover_color = HOVER

    def current_color(self):
        if self.disabled:
            return DISABLED
        if self.is_hovered(pygame.mouse.get_pos()):
            return self.hover_color
        return self.base_color

    def draw(self, surface):
        pygame.draw.rect(surface, self.current_color(), self.rect, border_radius=8)
        text_color = BLACK if self.disabled else WHITE
        text_surface = self.font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)

    def handle_event(self, event):
        """Run the callback on a left click. Returns the callback's result, or None."""
        if self.disabled:
            return None
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_hovered(event.pos):
                return self.callback()
        return None


class MenuButton(Button):
    """Larger-text button used on the main menu."""

    font_size = 36


def align_right(buttons, right, gap):
    """Lay out buttons left-to-right so the last one ends at x=right."""
    x = right - sum(b.rect.width for b in buttons) - gap * (len(buttons) - 1)
    for btn in buttons:
        btn.rect.x = x
        x += btn.rect.width + gap
