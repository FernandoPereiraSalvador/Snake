import pygame

from entities.food import Food
from entities.snake import Snake


class Game:
    def __init__(self):
        self.in_menu = True
        self.game_over = False

        self.food_count = 0

        self.snake = Snake()
        self.food = Food()

        self.last_update_time = pygame.time.get_ticks()

