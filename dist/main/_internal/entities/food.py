import random
from constants import SCREEN_WIDTH, CELL_SIZE, SCREEN_HEIGHT


class Food:
    """
    Class representing food in the Snake game.

    Food is placed in random positions within the playing area.
    """
    def __init__(self):
        """
        Initializes a new instance of the Food class.
        """
        self.position = None
        self.randomize_position()

    def randomize_position(self):
        """
        Generates a random position for the food within the playing area.

        The food is placed in a random cell on the game board.

        :return: None
        """

        # Subtract twice the size of the cell to keep it away from the borders.
        max_x = (SCREEN_WIDTH - 2 * CELL_SIZE) // CELL_SIZE
        max_y = (SCREEN_HEIGHT - 2 * CELL_SIZE) // CELL_SIZE
        self.position = (random.randint(1, max_x) * CELL_SIZE, random.randint(1, max_y) * CELL_SIZE)
