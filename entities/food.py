import random
from constants import SCREEN_WIDTH, CELL_SIZE, SCREEN_HEIGHT


class Food:
    def __init__(self):
        self.position = (random.randint(0, SCREEN_WIDTH // CELL_SIZE - 1) * CELL_SIZE,
                        random.randint(0, SCREEN_HEIGHT // CELL_SIZE - 1) * CELL_SIZE)

    def randomize_position(self):
        self.position = (random.randint(0, SCREEN_WIDTH // CELL_SIZE - 1) * CELL_SIZE,
                        random.randint(0, SCREEN_HEIGHT // CELL_SIZE - 1) * CELL_SIZE)
