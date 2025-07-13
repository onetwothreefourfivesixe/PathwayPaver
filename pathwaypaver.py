import pygame
import random
import sys

# ================================
# Initialization & Global Constants
# ================================
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 650    # Total screen height
HEADER_HEIGHT = 50     # Header area height
TILE_SIZE = 50         # Each grid cell is 50x50 pixels

# Grid dimensions for predefined level mode (16 x 12):
num_cols_level = SCREEN_WIDTH // TILE_SIZE      # 16
num_rows_level = (SCREEN_HEIGHT - HEADER_HEIGHT) // TILE_SIZE   # 600/50 = 12

# Maximum allowed road tiles:
max_tile = 30

# ================================
# Colors
# ================================
WHITE  = (255, 255, 255)
GRAY   = (220, 220, 220)
BLACK  = (0, 0, 0)
GREEN  = (0, 255, 0)
RED    = (255, 0, 0)
BLUE    = (0, 0, 255)
ACCENT = (0, 150, 255)
HOVER  = (50, 200, 255)
HEADER_BG = (200, 200, 200)  # Light gray header background

CAR_COLORS = [RED, (255, 255, 0), (255, 165, 0), (0, 128, 128)]
DEST_COLORS = CAR_COLORS  # Use the same for destinations

# ================================
# Setup Screen
# ================================
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pathway Paver")

# ================================
# Global Variables
# ================================
grid_data = []         # 2D list for the grid
cars = []              # List of Car objects
destinations_list = [] # List of Destination objects
header_buttons = []    # List of header buttons
current_tile_count = 0 # For tile placement
move_mode = False      # When True, the cars are moving
game_outcome = None    # "Success!" or "Fail!" once movement finishes
help_shown = False  # Track if the help screen has been shown
occupied_tiles = set()  # Tracks tiles occupied by cars

# ================================
# Level Presets
# ================================
levels = [
    {
        "name": "Level 1",
        "layout": [
            [0, 0, 84, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 94, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 86, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 96, 3],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ],
        "max_tiles": 30,
        "max_turns": 20
    },
    {
        "name": "Level 2",
        "layout": [
            [0, 0, 84, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 94, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 86, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 96, 3],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0],
            [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
        ],
        "max_tiles": 20,
        "max_turns": 16
    }, 
       {
        "name": "Level 3",
        "layout": [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0],
            [0, 0, 0, 86, 0, 0, 0, 0, 0, 0, 0, 94, 0, 0, 0, 0],
            [0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 84, 0, 0, 0, 0, 0, 0, 0, 96, 0, 0, 4, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ],
        "max_tiles": 21,
        "max_turns": 16
    },
    {
        "name": "Level 4",
        "layout": [
            [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 86, 0, 0, 0, 4, 0, 0, 0, 94, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 84, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 96, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0]
        ],
        "max_tiles": 24,
        "max_turns": 18
    }
]

# Track the current level
currentLevel = 0
completed_levels = [False] * len(levels)  # Initialize all levels as incomplete
completed_levels[0] = True  # Level 1 is always active

# ================================
# Classes
# ================================
class Car:
    def __init__(self, start_x, start_y):
        self.x = start_x
        self.y = start_y
        self.path = []     # List of (x, y) positions
        self.color = BLACK # Will be set appropriately
        self.id = None     # Car order id (0-based; display as id + 1)
        self.destination = None  # Tuple (x, y)
        self.reached = False

    def draw(self):
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
        font = pygame.font.Font(None, 20)
        text = font.render(f"{self.id + 1}", True, WHITE)
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
        """Uses BFS to find a path from start to destination."""
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
    def __init__(self, x, y, dest_id, color):
        self.x = x
        self.y = y
        self.id = dest_id
        self.color = color
        grid_data[y][x] = 3  # Mark destination with 3

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

class Button:
    def __init__(self, text, x, y, width, height, callback):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.callback = callback
        self.base_color = ACCENT
        self.hover_color = HOVER
        self.color = self.base_color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=8)
        font = pygame.font.Font(None, 24)
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_hovered(event.pos):
                self.callback()

# ================================
# Utility Functions
# ================================
def display_tile_count(tileCount, maxTile):
    font = pygame.font.Font(None, 36)
    text = font.render(f"Tiles: {tileCount}/{maxTile}", True, BLACK)
    screen.blit(text, (10, 10))

def draw_header(game_outcome):
    header_rect = pygame.Rect(0, 0, SCREEN_WIDTH, HEADER_HEIGHT)
    pygame.draw.rect(screen, HEADER_BG, header_rect)

    # Display the level name on the left
    level_name = levels[currentLevel]["name"]
    font = pygame.font.Font(None, 36)
    level_text = font.render(f"Level: {level_name}", True, BLACK)
    screen.blit(level_text, (10, 10))

    # Display the tile limit on the right
    tile_text = font.render(f"Tiles: {current_tile_count}/{levels[currentLevel]['max_tiles']}", True, BLACK)
    screen.blit(tile_text, (SCREEN_WIDTH - 500, 10))  # Adjusted position to the right

    # Display the turns left below the tile limit
    turn_text = font.render(f"Turns Left: {turns_left}", True, BLACK)
    screen.blit(turn_text, (SCREEN_WIDTH - 500, 30))  # Adjusted position to the right

    # Display the game outcome in the center
    if game_outcome is not None:
        outcome_text = font.render(game_outcome, True, BLACK)
        text_rect = outcome_text.get_rect(center=(SCREEN_WIDTH // 2, HEADER_HEIGHT // 2))
        screen.blit(outcome_text, text_rect)

    # Draw header buttons
    for btn in header_buttons:
        btn.draw(screen)

def handle_tile_click(mouse_x, mouse_y, tileCount):
    max_tiles = levels[currentLevel]["max_tiles"]
    if mouse_y < HEADER_HEIGHT:
        return tileCount
    grid_x = mouse_x // TILE_SIZE
    grid_y = (mouse_y - HEADER_HEIGHT) // TILE_SIZE
    if 0 <= grid_x < num_cols_level and 0 <= grid_y < num_rows_level:
        if grid_data[grid_y][grid_x] not in [2, 3, 4]:  # Prevent placing tiles on trees (4)
            if grid_data[grid_y][grid_x] == 0 and tileCount < max_tiles:
                grid_data[grid_y][grid_x] = 1
                return tileCount + 1
            elif grid_data[grid_y][grid_x] == 1:
                grid_data[grid_y][grid_x] = 0
                return tileCount - 1
    return tileCount

# ================================
# Predefined Level Mode Functions
# ================================
def load_level_objectives():
    global cars, destinations_list, grid_data, occupied_tiles
    cars = []
    destinations_list = []
    occupied_tiles = set()  # Reset occupied tiles

    level_data = levels[currentLevel]
    grid_data = [[level_data["layout"][y][x] for x in range(num_cols_level)] for y in range(num_rows_level)]
    for y, row in enumerate(level_data["layout"]):
        for x, tile in enumerate(row):
            if 80 <= tile <= 89:
                car_id = tile - 80
                car_color = CAR_COLORS[car_id % len(CAR_COLORS)]
                car = Car(x, y)
                car.id = car_id
                car.color = car_color
                cars.append(car)
                occupied_tiles.add((x, y))  # Mark the car's starting position as occupied
            elif 90 <= tile <= 99:
                dest_id = tile - 90
                dest_color = DEST_COLORS[dest_id % len(DEST_COLORS)]
                dest = Set_Destination(x, y, dest_id=dest_id, color=dest_color)
                destinations_list.append(dest)
    for car in cars:
        for dest in destinations_list:
            if car.color == dest.color:
                car.destination = (dest.x, dest.y)
                break

def draw_grid_level():
    for y in range(num_rows_level):
        for x in range(num_cols_level):
            rect = pygame.Rect(x * TILE_SIZE, HEADER_HEIGHT + y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            
            # Draw the grid background as green
            pygame.draw.rect(screen, WHITE, rect)  # Light green background
            
            # Draw grid lines
            pygame.draw.rect(screen, GRAY, rect, 1)
            
            if grid_data[y][x] == 1:  # Road tiles
                pygame.draw.rect(screen, GRAY, rect)
            elif grid_data[y][x] == 4:  # Trees
                pygame.draw.rect(screen, (0, 100, 0), rect)  # Dark green for trees

def load_level_game_loop():
    global current_tile_count, move_mode, game_outcome, header_buttons, turns_left, help_shown

    load_level_objectives()
    current_tile_count = 0
    move_mode = False
    game_outcome = None
    turns_left = levels[currentLevel]["max_turns"]  # Initialize turns_left to max_turns

    button_width = 100
    button_height = 30
    gap = 10
    total_buttons_width = 3 * button_width + 2 * gap
    start_x = SCREEN_WIDTH - total_buttons_width - 10
    restart_btn = Button("Restart", start_x, 10, button_width, button_height, restart_game_callback_level)
    level_btn = Button("Level Selection", start_x + button_width + gap, 10, button_width, button_height, level_selection_screen)
    help_btn = Button("Help", start_x + 2 * (button_width + gap), 10, button_width, button_height, help_screen)
    header_buttons = [restart_btn, level_btn, help_btn]

    # Automatically show the help screen the first time Level 1 is played
    if currentLevel == 0 and not help_shown:
        help_screen()
        help_shown = True

    clock = pygame.time.Clock()
    last_move_time = pygame.time.get_ticks()

    running = True
    while running:
        screen.fill(WHITE)
        draw_header(game_outcome)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[1] < HEADER_HEIGHT:
                    for btn in header_buttons:
                        btn.handle_event(event)
                elif not move_mode:
                    current_tile_count = handle_tile_click(event.pos[0], event.pos[1], current_tile_count)
            if not move_mode and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for car in cars:
                        path = car.find_path((car.x, car.y), car.destination)
                        print(f"Car {car.id} path:", path)
                    move_mode = True

        if move_mode:
            current_time = pygame.time.get_ticks()
            if current_time - last_move_time >= 500:
                process_turn()
                last_move_time = current_time

        draw_grid_level()
        for dest in destinations_list:
            dest.draw()
        for car in cars:
            car.draw()

        pygame.display.flip()
        clock.tick(60)

        # Show the result screen if the game ends
        if game_outcome in ["Success!", "Fail!"]:
            display_result_screen()
            running = False

    pygame.quit()

def restart_game_callback_level():
    load_level_game_loop()

def process_turn():
    global move_mode, game_outcome, turns_left, occupied_tiles

    # Decrease the number of turns left
    turns_left -= 1
    print(f"Turns left: {turns_left}")

    # Fail the level if no turns are left
    if turns_left < 0:
        move_mode = False
        game_outcome = "Fail!"
        print("No turns left! Game Over.")
        display_result_screen()
        return

    all_cars_reached = True
    new_occupied_tiles = set()  # Track tiles that will be occupied after this turn

    # Sort cars by ID to ensure lower ID cars move first
    for car in sorted(cars, key=lambda c: c.id):
        if not car.reached:
            if not car.path:
                # Fail the round if a car has no valid path
                move_mode = False
                game_outcome = "Fail!"
                print(f"Car {car.id} has no valid path! Game Over.")
                display_result_screen()
                return

            # Get the next position in the car's path
            next_position = car.path[0]

            # Check if the next position is already occupied
            if next_position in occupied_tiles or next_position in new_occupied_tiles:
                print(f"Car {car.id} cannot move to {next_position} because it is occupied!")
                all_cars_reached = False
                continue

            # Move the car to the next position
            car.path.pop(0)
            car.x, car.y = next_position
            new_occupied_tiles.add(next_position)

            # Check if the car has reached its destination
            if (car.x, car.y) == car.destination:
                car.reached = True
                print(f"Car {car.id} has reached its destination!")

        if not car.reached:
            all_cars_reached = False

    # Update the occupied tiles for the next turn
    occupied_tiles.clear()
    occupied_tiles.update(new_occupied_tiles)

    # If all cars have reached their destinations, end the game
    if all_cars_reached:
        move_mode = False
        game_outcome = "Success!"
        completed_levels[currentLevel] = True  # Mark the current level as completed
        if currentLevel < len(levels) - 1:
            completed_levels[currentLevel + 1] = True  # Unlock the next level
        print("All cars have reached their destinations!")
        display_result_screen()

def display_result_screen():
    global currentLevel

    # Create a semi-transparent overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  # Black with transparency
    screen.blit(overlay, (0, 0))

    # Display the result text
    font = pygame.font.Font(None, 72)
    result_text = font.render(game_outcome, True, WHITE)
    result_rect = result_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
    screen.blit(result_text, result_rect)

    # Create buttons for Restart, Next Level, and Main Menu
    button_width = 200
    button_height = 50
    gap = 20
    start_y = SCREEN_HEIGHT // 2

    restart_btn = Button("Restart Level", (SCREEN_WIDTH - button_width) // 2, start_y, button_width, button_height, restart_game_callback_level)

    # Only enable the "Next Level" button if the user succeeded
    if game_outcome == "Success!":
        next_level_btn = Button("Next Level", (SCREEN_WIDTH - button_width) // 2, start_y + button_height + gap, button_width, button_height, next_level_callback)
    else:
        next_level_btn = Button("Next Level (Locked)", (SCREEN_WIDTH - button_width) // 2, start_y + button_height + gap, button_width, button_height, lambda: None)
        next_level_btn.color = GRAY  # Disable the button visually

    main_menu_btn = Button("Main Menu", (SCREEN_WIDTH - button_width) // 2, start_y + 2 * (button_height + gap), button_width, button_height, main_menu_callback)

    # Draw buttons
    buttons = [restart_btn, next_level_btn, main_menu_btn]
    for btn in buttons:
        btn.draw(screen)

    pygame.display.flip()

    # Wait for user interaction
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn in buttons:
                    if btn.is_hovered(event.pos):
                        btn.handle_event(event)
                        waiting = False

def next_level_callback():
    global currentLevel
    if currentLevel < len(levels) - 1:
        currentLevel += 1
        load_level_game_loop()
    else:
        print("No more levels! Returning to main menu.")
        main_menu()

def main_menu_callback():
    main_menu()

def level_selection_screen():
    global currentLevel

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
    for i, level in enumerate(levels):
        col = i % cols
        row = i // cols
        x = start_x + col * (box_width + gap)
        y = start_y + row * (box_height + gap)
        rect = pygame.Rect(x, y, box_width, box_height)
        level_boxes.append((rect, i))

    clock = pygame.time.Clock()
    running = True
    while running:
        screen.fill(WHITE)

        # Draw title
        title_font = pygame.font.Font(None, 72)
        title_text = title_font.render("Level Selection", True, BLACK)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_text, title_rect)

        # Draw level boxes
        for rect, level_index in level_boxes:
            if completed_levels[level_index]:
                color = GREEN  # Fill with green if the level is completed
            else:
                color = GRAY  # Fill with gray if the level is not completed
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)  # Border

            # Draw level number
            font = pygame.font.Font(None, 36)
            text = font.render(str(level_index + 1), True, WHITE if completed_levels[level_index] else BLACK)
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

        # Draw back button
        back_btn = Button("Back", 10, 10, 100, 40, main_menu)
        back_btn.draw(screen)

        pygame.display.flip()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if a level box is clicked
                for rect, level_index in level_boxes:
                    if rect.collidepoint(event.pos) and completed_levels[level_index]:
                        currentLevel = level_index
                        load_level_game_loop()
                        return
                # Check if back button is clicked
                if back_btn.is_hovered(event.pos):
                    back_btn.handle_event(event)

        clock.tick(60)

# ================================
# Main Menu (Splash Screen)
# ================================
class MenuButton:
    def __init__(self, text, x, y, width, height, callback):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.callback = callback
        self.base_color = ACCENT
        self.hover_color = HOVER
        self.color = self.base_color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=8)
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_hovered(event.pos):
                self.callback()

def start_level_callback():
    load_level_game_loop()

def quit_game_callback():
    pygame.quit()
    sys.exit()

def main_menu():
    title_font = pygame.font.SysFont("Arial", 72, bold=True)
    button_width = 250
    button_height = 60
    gap = 20
    total_height = 3 * button_height + 2 * gap
    start_y = (SCREEN_HEIGHT - total_height) // 2 + 100

    level_btn = MenuButton("Level Selection", (SCREEN_WIDTH - button_width) // 2,
                           start_y, button_width, button_height, level_selection_screen)
    predefined_btn = MenuButton("Start", (SCREEN_WIDTH - button_width) // 2,
                                 start_y + button_height + gap, button_width, button_height, start_level_callback)
    quit_btn = MenuButton("Quit", (SCREEN_WIDTH - button_width) // 2,
                          start_y + 2 * (button_height + gap), button_width, button_height, quit_game_callback)
    buttons = [level_btn, predefined_btn, quit_btn]

    clock = pygame.time.Clock()
    running = True
    while running:
        screen.fill(WHITE)
        title_surface = title_font.render("Pathway Paver", True, BLACK)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(title_surface, title_rect)

        mouse_pos = pygame.mouse.get_pos()
        for btn in buttons:
            btn.color = btn.hover_color if btn.is_hovered(mouse_pos) else btn.base_color
            btn.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game_callback()
            for btn in buttons:
                btn.handle_event(event)

        pygame.display.flip()
        clock.tick(60)

def help_screen():
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(WHITE)

        # Draw title
        title_font = pygame.font.Font(None, 72)
        title_text = title_font.render("How to Play", True, BLACK)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_text, title_rect)

        # Draw instructions
        font = pygame.font.Font(None, 36)
        instructions = [
            "Goal: Get all the cars to their destinations.",
            "1. Place road tiles to create paths for the cars.",
            "2. Press SPACE to start moving the cars.",
            "3. Cars will follow the shortest path to their destination.",
            "4. You have a limited number of tiles and turns.",
            "5. Avoid obstacles like trees (dark green tiles).",
        ]
        for i, line in enumerate(instructions):
            text = font.render(line, True, BLACK)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 200 + i * 40))
            screen.blit(text, text_rect)

        # Draw back button
        def set_running_false():
            nonlocal running
            running = False
        back_btn = Button("Back", (SCREEN_WIDTH - 200) // 2, SCREEN_HEIGHT - 100, 200, 50, set_running_false)
        back_btn.draw(screen)

        pygame.display.flip()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.is_hovered(event.pos):
                    back_btn.handle_event(event)

        clock.tick(60)

# ================================
# Main Function
# ================================
def main():
    main_menu()

if __name__ == "__main__":
    main()