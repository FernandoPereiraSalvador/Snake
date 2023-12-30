import os
import sys

# Screen data
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
CELL_SIZE = 40

# Colors
SNAKE_COLOR = (55, 95, 197)  # Blue
GRID_COLOR_LIGHT = (173, 226, 85)  # Light blue
GRID_COLOR_DARK = (142, 198, 70)  # Dark green
FRAME_COLOR = (75, 123, 46)

# Data files
RECORD_FILE = os.path.join("resources/data", "record.txt")

# Dir
CURRENT_DIR = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))

# Sound files
BACKGROUND_MUSIC = os.path.join(CURRENT_DIR, 'resources', 'sound', 'music_theme.mp3')
APPLE_BIT = os.path.join(CURRENT_DIR, 'resources', 'sound', 'apple_bit.mp3')
DEAD_SOUND = os.path.join(CURRENT_DIR, 'resources', 'sound', 'dead.mp3')

# Images files
APPLE_IMAGE = os.path.join(CURRENT_DIR, 'resources', 'images', 'apple.png')
TROPHY_IMAGE = os.path.join(CURRENT_DIR, 'resources', 'images', 'trophy.png')
SOUND_TRUE = os.path.join(CURRENT_DIR, 'resources', 'images', 'sound_true.png')
SOUND_FALSE = os.path.join(CURRENT_DIR, 'resources', 'images', 'sound_false.png')

# Fps
UPDATE_INTERVAL = 200
