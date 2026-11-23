"""Out-of-level screens: main menu, level selection, and help.

main_menu and level_selection_screen return the next scene name (see scenes.py).
help_screen is a modal overlay: it returns None when closed, or scenes.QUIT if
the window was closed.
"""

import pygame

from . import scenes, state
from .config import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, GREEN, GRAY
from .display import screen
from .levels import levels
from .ui import Button, MenuButton


# ================================
# Main Menu (Splash Screen)
# ================================
def main_menu():
    title_font = pygame.font.SysFont("Arial", 72, bold=True)
    button_width = 250
    button_height = 60
    gap = 20
    total_height = 3 * button_height + 2 * gap
    start_y = (SCREEN_HEIGHT - total_height) // 2 + 100
    center_x = (SCREEN_WIDTH - button_width) // 2

    level_btn = MenuButton("Level Selection", center_x, start_y,
                           button_width, button_height, lambda: scenes.LEVEL_SELECT)
    start_btn = MenuButton("Start", center_x, start_y + button_height + gap,
                           button_width, button_height, lambda: scenes.PLAY)
    quit_btn = MenuButton("Quit", center_x, start_y + 2 * (button_height + gap),
                          button_width, button_height, lambda: scenes.QUIT)
    buttons = [level_btn, start_btn, quit_btn]

    clock = pygame.time.Clock()
    while True:
        screen.fill(WHITE)
        title_surface = title_font.render("Pathway Paver", True, BLACK)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(title_surface, title_rect)

        for btn in buttons:
            btn.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return scenes.QUIT
            for btn in buttons:
                next_scene = btn.handle_event(event)
                if next_scene:
                    return next_scene

        pygame.display.flip()
        clock.tick(60)


# ================================
# Level Selection
# ================================
def level_selection_screen():
    # Define box dimensions
    box_width = 100
    box_height = 100
    gap = 20
    cols = 4  # Number of columns in the grid
    rows = (len(levels) + cols - 1) // cols  # Calculate rows based on the number of levels
    start_x = (SCREEN_WIDTH - (cols * box_width + (cols - 1) * gap)) // 2
    start_y = (SCREEN_HEIGHT - (rows * box_height + (rows - 1) * gap)) // 2

    # Create level boxes
    level_boxes = []
    for i in range(len(levels)):
        col = i % cols
        row = i // cols
        x = start_x + col * (box_width + gap)
        y = start_y + row * (box_height + gap)
        rect = pygame.Rect(x, y, box_width, box_height)
        level_boxes.append((rect, i))

    back_btn = Button("Back", 10, 10, 100, 40, lambda: scenes.MAIN_MENU)
    title_font = pygame.font.Font(None, 72)
    font = pygame.font.Font(None, 36)

    clock = pygame.time.Clock()
    while True:
        screen.fill(WHITE)

        # Draw title
        title_text = title_font.render("Level Selection", True, BLACK)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_text, title_rect)

        # Draw level boxes
        for rect, level_index in level_boxes:
            unlocked = state.completed_levels[level_index]
            color = GREEN if unlocked else GRAY
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)  # Border

            # Draw level number
            text = font.render(str(level_index + 1), True, WHITE if unlocked else BLACK)
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

        back_btn.draw(screen)
        pygame.display.flip()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return scenes.QUIT
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if an unlocked level box is clicked
                for rect, level_index in level_boxes:
                    if rect.collidepoint(event.pos) and state.completed_levels[level_index]:
                        state.currentLevel = level_index
                        return scenes.PLAY
                next_scene = back_btn.handle_event(event)
                if next_scene:
                    return next_scene

        clock.tick(60)


# ================================
# Help Screen
# ================================
HELP_INSTRUCTIONS = [
    "Goal: Get all the cars to their destinations.",
    "1. Place road tiles to create paths for the cars.",
    "2. Press SPACE to start moving the cars.",
    "3. Cars will follow the shortest path to their destination.",
    "4. You have a limited number of tiles and turns.",
    "5. Avoid obstacles like trees (dark green tiles).",
]


def help_screen():
    """Show instructions until Back is clicked. Returns scenes.QUIT if the window is closed."""
    back_btn = Button("Back", (SCREEN_WIDTH - 200) // 2, SCREEN_HEIGHT - 100, 200, 50, lambda: True)
    title_font = pygame.font.Font(None, 72)
    font = pygame.font.Font(None, 36)

    clock = pygame.time.Clock()
    while True:
        screen.fill(WHITE)

        # Draw title
        title_text = title_font.render("How to Play", True, BLACK)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_text, title_rect)

        # Draw instructions
        for i, line in enumerate(HELP_INSTRUCTIONS):
            text = font.render(line, True, BLACK)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 200 + i * 40))
            screen.blit(text, text_rect)

        back_btn.draw(screen)
        pygame.display.flip()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return scenes.QUIT
            if back_btn.handle_event(event):
                return None

        clock.tick(60)
