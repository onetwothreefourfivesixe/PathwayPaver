"""Mutable game state shared across modules.

Always access these as attributes of this module (``state.grid_data``),
never via ``from .state import grid_data``, so that reassignments made
in one module are visible everywhere else.
"""

from .levels import levels

grid_data = []          # 2D list for the grid
cars = []               # List of Car objects
destinations_list = []  # List of Set_Destination objects
header_buttons = []     # List of header buttons
current_tile_count = 0  # For tile placement
move_mode = False       # When True, the cars are moving
game_outcome = None     # "Success!" or "Fail!" once movement finishes
help_shown = False      # Track if the help screen has been shown
occupied_tiles = set()  # Tracks tiles occupied by cars
turns_left = 0          # Turns remaining in the current level
paths_dirty = True      # True when road tiles changed and path previews need recomputing
all_connected = False   # True when every car has a path to its house (planning phase)

# Level progression
currentLevel = 0
completed_levels = [False] * len(levels)  # Initialize all levels as incomplete
completed_levels[0] = True                # Level 1 is always active
