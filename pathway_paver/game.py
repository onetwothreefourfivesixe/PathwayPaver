"""In-level gameplay: the main game loop, turn processing, and result screen."""

import pygame

from . import scenes, state
from .config import SCREEN_WIDTH, SCREEN_HEIGHT, HEADER_HEIGHT, WHITE
from .display import screen
from .grid import load_level_objectives, draw_grid_level, handle_tile_click
from .hud import draw_header, draw_message_bar
from .levels import levels
from .notifications import notify, clear as clear_notifications
from .screens import help_screen
from .ui import Button, align_right

TURN_INTERVAL_MS = 500  # Delay between car moves
PREVIEW_SPREAD = 6      # Pixels between overlapping route preview lines


def update_path_previews():
    """Recompute every car's route if the road layout changed since last time."""
    if not state.paths_dirty:
        return
    for car in state.cars:
        car.find_path((car.x, car.y), car.destination)
    state.all_connected = all(car.path for car in state.cars)
    state.paths_dirty = False


def draw_path_previews():
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    count = len(state.cars)
    for i, car in enumerate(state.cars):
        offset = int((i - (count - 1) / 2) * PREVIEW_SPREAD)
        car.draw_path_preview(overlay, offset)
    screen.blit(overlay, (0, 0))


def play_level():
    """Load the current level and run it. Returns the next scene name."""
    load_level_objectives()
    state.current_tile_count = 0
    state.move_mode = False
    state.game_outcome = None
    state.turns_left = levels[state.currentLevel]["max_turns"]
    state.paths_dirty = True
    state.all_connected = False
    clear_notifications()

    button_height = 30
    button_y = (HEADER_HEIGHT - button_height) // 2
    restart_btn = Button("Restart", 0, button_y, None, button_height, lambda: scenes.PLAY)
    level_btn = Button("Levels", 0, button_y, None, button_height, lambda: scenes.LEVEL_SELECT)
    help_btn = Button("Help", 0, button_y, None, button_height, help_screen)
    state.header_buttons = [restart_btn, level_btn, help_btn]
    align_right(state.header_buttons, right=SCREEN_WIDTH - 10, gap=8)

    # Automatically show the help screen the first time Level 1 is played
    if state.currentLevel == 0 and not state.help_shown:
        state.help_shown = True
        if help_screen() == scenes.QUIT:
            return scenes.QUIT

    clock = pygame.time.Clock()
    last_move_time = pygame.time.get_ticks()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return scenes.QUIT
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[1] < HEADER_HEIGHT:
                    for btn in state.header_buttons:
                        next_scene = btn.handle_event(event)
                        if next_scene:
                            return next_scene
                elif not state.move_mode:
                    state.current_tile_count = handle_tile_click(event.pos[0], event.pos[1], state.current_tile_count)
            if not state.move_mode and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    state.paths_dirty = True
                    update_path_previews()
                    clear_notifications()
                    state.move_mode = True

        if state.move_mode:
            current_time = pygame.time.get_ticks()
            if current_time - last_move_time >= TURN_INTERVAL_MS:
                process_turn()
                last_move_time = current_time

        planning = not state.move_mode and state.game_outcome is None
        if planning:
            update_path_previews()

        screen.fill(WHITE)
        draw_header()
        draw_grid_level()
        if planning:
            draw_path_previews()
        for dest in state.destinations_list:
            dest.draw()
        for car in state.cars:
            car.draw(planning=planning)
        draw_message_bar()

        pygame.display.flip()
        clock.tick(60)

        # Show the result screen once the level has ended
        if state.game_outcome is not None:
            return display_result_screen()


def process_turn():
    """Advance every car one step along its path and set state.game_outcome if the level ends."""
    # Decrease the number of turns left
    state.turns_left -= 1

    # Fail the level if no turns are left
    if state.turns_left < 0:
        state.move_mode = False
        state.game_outcome = "Fail!"
        notify("Out of turns!")
        return

    all_cars_reached = True
    new_occupied_tiles = set()  # Track tiles that will be occupied after this turn

    # Sort cars by ID to ensure lower ID cars move first
    for car in sorted(state.cars, key=lambda c: c.id):
        if not car.reached:
            if not car.path:
                # Fail the round if a car has no valid path
                state.move_mode = False
                state.game_outcome = "Fail!"
                notify(f"Car {car.label} has no path to its house!")
                return

            # Get the next position in the car's path
            next_position = car.path[0]

            # Check if the next position is already occupied
            if next_position in state.occupied_tiles or next_position in new_occupied_tiles:
                car.blocked = True
                all_cars_reached = False
                continue

            # Move the car to the next position
            car.path.pop(0)
            car.blocked = False
            car.x, car.y = next_position
            new_occupied_tiles.add(next_position)

            # Check if the car has reached its destination
            if (car.x, car.y) == car.destination:
                car.reached = True
                notify(f"Car {car.label} is home!")

        if not car.reached:
            all_cars_reached = False

    # Update the occupied tiles for the next turn
    state.occupied_tiles.clear()
    state.occupied_tiles.update(new_occupied_tiles)

    # If all cars have reached their destinations, end the game
    if all_cars_reached:
        state.move_mode = False
        state.game_outcome = "Success!"
        state.completed_levels[state.currentLevel] = True  # Mark the current level as completed
        if state.currentLevel < len(levels) - 1:
            state.completed_levels[state.currentLevel + 1] = True  # Unlock the next level


def _next_level():
    if state.currentLevel < len(levels) - 1:
        state.currentLevel += 1
        return scenes.PLAY
    return scenes.MAIN_MENU


def display_result_screen():
    """Overlay the outcome and wait for a choice. Returns the next scene name."""
    # Create a semi-transparent overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  # Black with transparency
    screen.blit(overlay, (0, 0))

    # Display the result text
    font = pygame.font.Font(None, 72)
    result_text = font.render(state.game_outcome, True, WHITE)
    result_rect = result_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
    screen.blit(result_text, result_rect)

    # Create buttons for Restart, Next Level, and Main Menu
    button_width = 200
    button_height = 50
    gap = 20
    start_y = SCREEN_HEIGHT // 2
    center_x = (SCREEN_WIDTH - button_width) // 2

    restart_btn = Button("Restart Level", center_x, start_y, button_width, button_height, lambda: scenes.PLAY)

    # Only enable the "Next Level" button if the user succeeded
    if state.game_outcome == "Success!":
        next_level_btn = Button("Next Level", center_x, start_y + button_height + gap, button_width, button_height, _next_level)
    else:
        next_level_btn = Button("Next Level (Locked)", center_x, start_y + button_height + gap, button_width, button_height, lambda: None, disabled=True)

    main_menu_btn = Button("Main Menu", center_x, start_y + 2 * (button_height + gap), button_width, button_height, lambda: scenes.MAIN_MENU)

    buttons = [restart_btn, next_level_btn, main_menu_btn]
    background = screen.copy()

    # Redraw every frame so hover colors update; wait for the user to pick an option
    clock = pygame.time.Clock()
    while True:
        screen.blit(background, (0, 0))
        for btn in buttons:
            btn.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return scenes.QUIT
            for btn in buttons:
                next_scene = btn.handle_event(event)
                if next_scene:
                    return next_scene
        clock.tick(60)
