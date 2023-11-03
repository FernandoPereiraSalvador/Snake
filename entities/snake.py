from constants import SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE


class Snake:
    """
    Class representing the snake in the Snake game.

    The snake is a set of segments that moves across the game board.
    """
    def __init__(self):
        """
        Initializes a new instance of the Snake class.

        Atributes:
        - body (list): A list of coordinates (x, y) representing the segments of the snake's body.
        - direction (tuple): The current direction in which the snake is moving.

        """
        # Coordenadas iniciales
        initial_x = (SCREEN_WIDTH // 2 // CELL_SIZE -4) * CELL_SIZE
        initial_y = (SCREEN_HEIGHT // 2 // CELL_SIZE) * CELL_SIZE

        self.body = [(initial_x, initial_y)]

        self.direction = (1,0)

        # Le añadimos un segmento extra para que comienze con 2
        self.grow()

    def reset(self):
        """
        Resets the snake to its initial state.

        The snake returns to a single segment in the initial position and moves to the right.

        :return: None
        """

        # Coordenadas iniciales
        initial_x = (SCREEN_WIDTH // 2 // CELL_SIZE - 4) * CELL_SIZE
        initial_y = (SCREEN_HEIGHT // 2 // CELL_SIZE) * CELL_SIZE

        self.body = [(initial_x, initial_y)]
        self.direction = (1, 0)
        self.grow()

    def move(self):
        """
        Moves the snake one step in its current direction.

        The snake moves one step forward and its head moves in the current direction. The body segments follow the head.

        :return: None
        """

        # Calculate the new coordinates for the head of the snake based on its current direction.
        new_head = (
            (self.body[0][0] + self.direction[0] * CELL_SIZE) % SCREEN_WIDTH,
            (self.body[0][1] + self.direction[1] * CELL_SIZE) % SCREEN_HEIGHT
        )

        # Update the snake's body by replacing the old head with the new head.
        self.body = [new_head] + self.body[:-1]

    def change_direction(self, new_direction):
        """
        Changes the snake's direction of movement

        If the new direction is not opposite to the current direction, the direction in which the snake moves is changed.

        :param new_direction: The new direction in which the snake will move (left, right, up or down).
        :return: None
        """
        if new_direction[0] * -1 != self.direction[0] or new_direction[1] * -1 != self.direction[1]:
            self.direction = new_direction

    def grow(self):
        """
        It makes the snake grow by adding a new segment to the end of its body.

        :return: None
        """
        self.body.append(self.body[-1])

    def __iter__(self):
        """
        Returns an iterator for the Snake's body segments.

        :return: An iterator object for the Snake's body segments.
        """
        return iter(self.body)