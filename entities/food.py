import random
from constants import SCREEN_WIDTH, CELL_SIZE, SCREEN_HEIGHT


class Food:
    def __init__(self):
        self.position = None
        self.randomize_position()

    def randomize_position(self):
        max_x = (SCREEN_WIDTH - 2 * CELL_SIZE) // CELL_SIZE  # Resta dos veces el tamaño de la celda
        max_y = (SCREEN_HEIGHT - 2 * CELL_SIZE) // CELL_SIZE  # Resta dos veces el tamaño de la celda
        self.position = (random.randint(1, max_x) * CELL_SIZE, random.randint(1, max_y) * CELL_SIZE)
