"""Level loading, grid rendering, and road-tile placement."""

import pygame

from . import state
from .config import (
    TILE_SIZE, HEADER_HEIGHT, num_cols_level, num_rows_level,
    WHITE, GRAY, TREE_COLOR, CAR_COLORS, DEST_COLORS,
)
from .display import screen
from .entities import Car, Set_Destination
from .levels import levels
from .notifications import notify


def load_level_objectives():
    """Build the grid, cars, and destinations for the current level."""
    state.cars = []
    state.destinations_list = []
    state.occupied_tiles = set()  # Reset occupied tiles

    level_data = levels[state.currentLevel]
    state.grid_data = [[level_data["layout"][y][x] for x in range(num_cols_level)] for y in range(num_rows_level)]
    for y, row in enumerate(level_data["layout"]):
        for x, tile in enumerate(row):
            if 80 <= tile <= 89:
                car_id = tile - 80
                car_color = CAR_COLORS[car_id % len(CAR_COLORS)]
                car = Car(x, y)
                car.id = car_id
                car.color = car_color
                state.cars.append(car)
                state.occupied_tiles.add((x, y))  # Mark the car's starting position as occupied
            elif 90 <= tile <= 99:
                dest_id = tile - 90
                dest_color = DEST_COLORS[dest_id % len(DEST_COLORS)]
                dest = Set_Destination(x, y, dest_id=dest_id, color=dest_color)
                state.destinations_list.append(dest)
    for car in state.cars:
        for dest in state.destinations_list:
            if car.color == dest.color:
                car.destination = (dest.x, dest.y)
                break


def draw_grid_level():
    for y in range(num_rows_level):
        for x in range(num_cols_level):
            rect = pygame.Rect(x * TILE_SIZE, HEADER_HEIGHT + y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

            # Draw the grid background
            pygame.draw.rect(screen, WHITE, rect)

            # Draw grid lines
            pygame.draw.rect(screen, GRAY, rect, 1)

            if state.grid_data[y][x] == 1:  # Road tiles
                pygame.draw.rect(screen, GRAY, rect)
            elif state.grid_data[y][x] == 4:  # Trees
                pygame.draw.rect(screen, TREE_COLOR, rect)


def handle_tile_click(mouse_x, mouse_y, tileCount):
    """Toggle a road tile at the clicked cell. Returns the new tile count.

    Shows a message when the placement isn't allowed, and marks path
    previews for recomputation when the grid changes.
    """
    grid_data = state.grid_data
    max_tiles = levels[state.currentLevel]["max_tiles"]
    if mouse_y < HEADER_HEIGHT:
        return tileCount
    grid_x = mouse_x // TILE_SIZE
    grid_y = (mouse_y - HEADER_HEIGHT) // TILE_SIZE
    if not (0 <= grid_x < num_cols_level and 0 <= grid_y < num_rows_level):
        return tileCount

    tile = grid_data[grid_y][grid_x]
    if tile == 1:
        grid_data[grid_y][grid_x] = 0
        state.paths_dirty = True
        return tileCount - 1
    if tile == 0:
        if tileCount >= max_tiles:
            notify("No tiles left. Click a road to remove it.")
            return tileCount
        grid_data[grid_y][grid_x] = 1
        state.paths_dirty = True
        return tileCount + 1

    if tile == 4:
        notify("Can't build on trees")
    elif tile in (2, 3) or 90 <= tile <= 99:
        notify("Can't build on a house")
    elif 80 <= tile <= 89:
        notify("Can't build under a car")
    return tileCount
