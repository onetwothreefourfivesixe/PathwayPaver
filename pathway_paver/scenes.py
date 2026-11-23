"""Scene names used for navigation.

Every top-level screen function returns the name of the scene to show next.
The loop in __main__.py runs the matching function, so screens never call
each other directly and the call stack never grows. The help screen is the
one exception: it is a modal overlay that simply returns to its caller.
"""

MAIN_MENU = "main_menu"
LEVEL_SELECT = "level_select"
PLAY = "play"
QUIT = "quit"
