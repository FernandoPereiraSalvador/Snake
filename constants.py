import os

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
CELL_SIZE = 40
SNAKE_COLOR = (55, 95, 197)  # Azul
GRID_COLOR_LIGHT = (173, 226, 85)  # Azul claro
GRID_COLOR_DARK = (142, 198, 70)  # Verde oscuro
FRAME_COLOR = (75, 123, 46)

RECORD_FILE = os.path.join("resources/data", "record.txt")
BACKGROUND_MUSIC = os.path.join("resources/sound", "music_theme.mp3")
APPLE_BIT = os.path.join("resources/sound", "apple_bit.mp3")
DEAD_SOUND = os.path.join("resources/sound", "dead.mp3")

UPDATE_INTERVAL = 200