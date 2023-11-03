import pygame

from entities.food import Food
from entities.snake import Snake


class Game:
    """
    Class representing the game.
    """
    def __init__(self):
        """
        Initializes a new instance of the game.

        The initial configuration includes the game in menu mode, not in "game over" mode,
        a food count equal to zero, an initialized snake and food,
        a tracking of the time of the last update, and the status of the activated sound.

        Atributes:
        - in_menu (bool): indicates whether the game is in the main menu.
        - game_over (bool): Indicates if the game is over.
        - food_count (int): The number of apples consumed by the snake.
        - snake (Snake): Instance of the snake in the game.
        - food (Food): Instance of the food in the game.
        - last_update_time (int): The time of the last update of the game.
        - sond (bool): Indicates if the sound of the game is activated (True) or deactivated (False).
        """

        self.in_menu = True
        self.game_over = False
        self.food_count = 0
        self.snake = Snake()
        self.food = Food()
        self.last_update_time = pygame.time.get_ticks()
        self.sond = True

    def toggle_music(self):
        """
        Toggles the game sound status between on and off.

        If the sound is activated, this function deactivates the sound and pauses the background music.
        If the sound is deactivated, this function activates the sound and resumes the background music.

        :return: None
        """
        self.sond = not self.sond
        if self.sond:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()

