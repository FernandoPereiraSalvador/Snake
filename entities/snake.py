from constants import SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE


class Snake:
    def __init__(self):
        initial_x = (SCREEN_WIDTH // 2 // CELL_SIZE) * CELL_SIZE
        initial_y = (SCREEN_HEIGHT // 2 // CELL_SIZE) * CELL_SIZE
        self.body = [(initial_x, initial_y)]
        self.direction = (1,0)

    def move(self):

        new_head = (
            (self.body[0][0] + self.direction[0] * CELL_SIZE) % SCREEN_WIDTH,
            (self.body[0][1] + self.direction[1] * CELL_SIZE) % SCREEN_HEIGHT
        )

        self.body = [new_head] + self.body[:-1]

    def change_direction(self, new_direction):
        if new_direction[0] * -1 != self.direction[0] or new_direction[1] * -1 != self.direction[1]:
            self.direction = new_direction

    def grow(self):
        self.body.append(self.body[-1])

    def __iter__(self):
        return iter(self.body)