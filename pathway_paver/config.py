"""Global constants: screen layout, grid dimensions, and colors."""

# ================================
# Screen & Grid Dimensions
# ================================
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 650    # Total screen height
HEADER_HEIGHT = 50     # Header area height
TILE_SIZE = 50         # Each grid cell is 50x50 pixels

# Grid dimensions for predefined level mode (16 x 12):
num_cols_level = SCREEN_WIDTH // TILE_SIZE                      # 16
num_rows_level = (SCREEN_HEIGHT - HEADER_HEIGHT) // TILE_SIZE   # 600/50 = 12

# Maximum allowed road tiles:
max_tile = 30

# ================================
# Tile codes used in level layouts
# ================================
# 0      empty
# 1      road (placed by the player)
# 3      destination (house)
# 4      tree (obstacle)
# 80-89  car start; car id = code - 80
# 90-99  destination; destination id = code - 90

# ================================
# Colors
# ================================
WHITE  = (255, 255, 255)
GRAY   = (220, 220, 220)
BLACK  = (0, 0, 0)
GREEN  = (0, 255, 0)
RED    = (255, 0, 0)
BLUE   = (0, 0, 255)
ACCENT = (0, 150, 255)
HOVER  = (50, 200, 255)
HEADER_BG = (200, 200, 200)  # Light gray header background
HEADER_DIVIDER = (160, 160, 160)
TREE_COLOR = (0, 100, 0)     # Dark green for trees
WARNING = (210, 30, 30)      # Low turns/tiles, cars with no path
WAITING = (60, 60, 60)       # Outline on a car blocked by another car
DISABLED = GRAY              # Disabled button fill
MESSAGE_BG = (30, 30, 30)    # Message bar background

CAR_COLORS = [RED, (255, 255, 0), (255, 165, 0), (0, 128, 128)]
DEST_COLORS = CAR_COLORS  # Use the same for destinations

# ================================
# Fonts (pygame default font, sizes in px)
# ================================
FONT_HEADER = 28
FONT_BUTTON = 24
FONT_MESSAGE = 26
FONT_LABEL = 20   # Numbers on cars and houses

# ================================
# UI tuning
# ================================
BUTTON_PADDING_X = 14       # Horizontal padding for auto-sized buttons
LOW_TURNS_THRESHOLD = 3     # Turns counter turns red at or below this
MESSAGE_DURATION_MS = 2000  # How long a message stays on screen
MESSAGE_FADE_MS = 400       # Fade-out time at the end of a message
PREVIEW_ALPHA = 140         # Opacity of the path preview lines
PREVIEW_WIDTH = 6           # Thickness of the path preview lines
