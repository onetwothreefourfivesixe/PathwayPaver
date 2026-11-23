"""Game entities that live on the grid: cars and their destination houses."""

import pygame

from . import state
from .config import (
    TILE_SIZE, HEADER_HEIGHT, BLACK, BLUE, WARNING, WAITING,
    FONT_LABEL, PREVIEW_ALPHA, PREVIEW_WIDTH,
)
from .display import screen
from .ui import readable_text_color


def tile_center(x, y):
    """Pixel center of grid cell (x, y)."""
    return (x * TILE_SIZE + TILE_SIZE // 2, HEADER_HEIGHT + y * TILE_SIZE + TILE_SIZE // 2)


class Car:
    def __init__(self, start_x, start_y):
        self.x = start_x
        self.y = start_y
        self.path = []     # List of (x, y) positions
        self.color = BLACK # Will be set appropriately
        self.id = None     # Car order id (0-based; display as id + 1)
        self.destination = None  # Tuple (x, y)
        self.reached = False
        self.blocked = False     # True while waiting for another car to move out of the way

    @property
    def label(self):
        """The number shown to the player."""
        return self.id + 1

    def draw_path_preview(self, surface, offset=0):
        """Draw the planned route as a translucent line on an SRCALPHA surface.

        offset shifts the line a few pixels so overlapping routes stay visible.
        """
        if self.reached or not self.path:
            return
        points = [tile_center(self.x, self.y)] + [tile_center(px, py) for px, py in self.path]
        points = [(px + offset, py + offset) for px, py in points]
        color = (*self.color[:3], PREVIEW_ALPHA)
        pygame.draw.lines(surface, color, False, points, PREVIEW_WIDTH)
        pygame.draw.circle(surface, color, points[-1], PREVIEW_WIDTH)

    def draw(self, planning=False):
        """Draw the car. In planning mode, a car with no route gets a red warning outline."""
        # Skip drawing if the car has reached its destination
        if self.reached:
            return

        # Calculate the car's position and size
        car_x = self.x * TILE_SIZE + TILE_SIZE // 6
        car_y = HEADER_HEIGHT + self.y * TILE_SIZE + TILE_SIZE // 6
        car_width = TILE_SIZE * 2 // 3
        car_height = TILE_SIZE * 2 // 3

        # Draw the car body (rounded rectangle)
        car_rect = pygame.Rect(car_x, car_y, car_width, car_height)
        pygame.draw.rect(screen, self.color, car_rect, border_radius=8)

        # Warning outlines: no route (planning) or waiting on another car (moving)
        if planning and not self.path:
            pygame.draw.rect(screen, WARNING, car_rect.inflate(8, 8), 3, border_radius=10)
        elif self.blocked:
            pygame.draw.rect(screen, WAITING, car_rect.inflate(8, 8), 3, border_radius=10)

        # Draw the wheels (small black circles)
        wheel_radius = TILE_SIZE // 10
        wheel_offset_x = TILE_SIZE // 1.5
        wheel_offset_y = TILE_SIZE // 1.5

        # Front-left wheel
        pygame.draw.circle(screen, BLACK, (car_x + wheel_offset_x, car_y + car_height - wheel_offset_y), wheel_radius)
        # Front-right wheel
        pygame.draw.circle(screen, BLACK, (car_x + car_width - wheel_offset_x, car_y + car_height - wheel_offset_y), wheel_radius)
        # Rear-left wheel
        pygame.draw.circle(screen, BLACK, (car_x + wheel_offset_x, car_y + wheel_offset_y), wheel_radius)
        # Rear-right wheel
        pygame.draw.circle(screen, BLACK, (car_x + car_width - wheel_offset_x, car_y + wheel_offset_y), wheel_radius)

        # Draw the car ID inside the car body
        font = pygame.font.Font(None, FONT_LABEL)
        text = font.render(str(self.label), True, readable_text_color(self.color))
        text_rect = text.get_rect(center=car_rect.center)
        screen.blit(text, text_rect)

        # Draw the windshield to indicate direction
        if self.path:
            next_x, next_y = self.path[0]  # Get the next position in the path
            dx = next_x - self.x
            dy = next_y - self.y

            # Determine the windshield position based on direction
            if dx == 1:  # Moving right
                windshield_rect = pygame.Rect(car_x + car_width - 5, car_y + car_height // 4, 5, car_height // 2)
            elif dx == -1:  # Moving left
                windshield_rect = pygame.Rect(car_x, car_y + car_height // 4, 5, car_height // 2)
            elif dy == 1:  # Moving down
                windshield_rect = pygame.Rect(car_x + car_width // 4, car_y + car_height - 5, car_width // 2, 5)
            elif dy == -1:  # Moving up
                windshield_rect = pygame.Rect(car_x + car_width // 4, car_y, car_width // 2, 5)
            else:
                windshield_rect = None

            # Draw the windshield
            if windshield_rect:
                pygame.draw.rect(screen, BLUE, windshield_rect)

    def find_path(self, start, destination):
        """Uses BFS to find a path from start to destination.

        Sets self.path to the route (excluding start), or [] if there is none.
        """
        self.path = []
        grid_data = state.grid_data
        queue = [(start[0], start[1], [])]
        visited = set()
        current_rows = len(grid_data)
        current_cols = len(grid_data[0]) if current_rows > 0 else 0
        while queue:
            x, y, path = queue.pop(0)
            if (x, y) == destination:
                self.path = path + [(x, y)]
                return self.path
            if (x, y) in visited:
                continue
            visited.add((x, y))
            for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < current_cols and 0 <= ny < current_rows:
                    if grid_data[ny][nx] in [1, 3]:
                        queue.append((nx, ny, path + [(nx, ny)]))
        return []


class Set_Destination:
    """A destination house. Registers itself on the grid as tile code 3."""

    def __init__(self, x, y, dest_id, color):
        self.x = x
        self.y = y
        self.id = dest_id
        self.color = color
        state.grid_data[y][x] = 3  # Mark destination with 3

    def draw(self):
        # Calculate the position and size of the house
        house_x = self.x * TILE_SIZE
        house_y = HEADER_HEIGHT + self.y * TILE_SIZE
        house_width = TILE_SIZE
        house_height = TILE_SIZE

        # Draw the base of the house (rectangle)
        base_rect = pygame.Rect(house_x + house_width // 6, house_y + house_height // 3, house_width * 2 // 3, house_height * 2 // 3)
        pygame.draw.rect(screen, self.color, base_rect)

        # Draw the roof of the house (triangle)
        roof_points = [
            (house_x + house_width // 2, house_y),  # Top point of the triangle
            (house_x + house_width // 6, house_y + house_height // 3),  # Bottom-left point
            (house_x + house_width * 5 // 6, house_y + house_height // 3)  # Bottom-right point
        ]
        pygame.draw.polygon(screen, self.color, roof_points)

        # Draw the matching car's number on the house
        font = pygame.font.Font(None, FONT_LABEL)
        text = font.render(str(self.id + 1), True, readable_text_color(self.color))
        screen.blit(text, text.get_rect(center=base_rect.center))
