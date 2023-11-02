import os
import time

import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE, GRID_COLOR_DARK, GRID_COLOR_LIGHT, SNAKE_COLOR, \
    FRAME_COLOR, UPDATE_INTERVAL, BACKGROUND_MUSIC, APPLE_BIT, DEAD_SOUND, APPLE_IMAGE, TROPHY_IMAGE
from game import Game

from utils.record_utils import get_record, save_record

def main():
    """
    Main function executing the snake game.

    Initialize Pygame and configure the game window. Loads the necessary resources,
    starts the music and the main game loop. Handles events, snake controls,
    and game logic. Draws the game state on the screen.


    :return:
    """

    # Initializes the Pygame game engine
    pygame.init()
    # Initializes Pygame's sound mixing module
    pygame.mixer.init()

    # Creates the game window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Game")
    icon_image = pygame.image.load(APPLE_IMAGE)
    pygame.display.set_icon(icon_image)

    # Initializes a new game instance
    game = Game()

    # Start the music
    apple_sound = pygame.mixer.Sound(APPLE_BIT)
    dead_sound = pygame.mixer.Sound(DEAD_SOUND)
    pygame.mixer.music.load(BACKGROUND_MUSIC)
    pygame.mixer.music.play(-1)  # Playing music in an infinite loop

    # Main game loop
    while True:
        events = pygame.event.get()  # Get events at each iteration

        for event in events:
            # Exits the loop if the game window is closed.
            if event.type == pygame.QUIT:
                pygame.quit()
                pygame.quit()
                return
            # Show the main menu if we are in the
            if game.in_menu:
                start_game = menu(screen, events)
                if start_game:
                    game.in_menu = False

            # If the player clicks on one of the arrows the snake moves
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.snake.change_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    game.snake.change_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    game.snake.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    game.snake.change_direction((1, 0))

            # Deactivate/activate game music and sounds
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if pygame.Rect(CELL_SIZE * 13 + 10, CELL_SIZE // 2 - 13, CELL_SIZE - 15, CELL_SIZE - 15).collidepoint(event.pos):
                        game.toggle_music()

        # If we are not in the main menu and the game has not finished, we start the loop to play.
        if not game.in_menu and not game.game_over:
            draw(screen, game)
            # Draw the snake
            for i, segment in enumerate(game.snake):
                if i == 0:
                    # Draw the rectangle of the head in the color of the snake.
                    pygame.draw.rect(screen, SNAKE_COLOR, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))

                    # Determine the position of the eyes according to head orientation
                    eye_positions = []
                    if game.snake.direction == (0, -1): # Up
                        eye_positions = [(segment[0] + CELL_SIZE // 3, segment[1] + CELL_SIZE // 4),
                                         (segment[0] + 2 * CELL_SIZE // 3, segment[1] + CELL_SIZE // 4)]

                    elif game.snake.direction == (0, 1): # Down
                        eye_positions = [(segment[0] + CELL_SIZE // 3, segment[1] + 2 * CELL_SIZE // 3),
                                         (segment[0] + 2 * CELL_SIZE // 3, segment[1] + 2 * CELL_SIZE // 3)]

                    elif game.snake.direction == (-1, 0): #Left
                        eye_positions = [(segment[0] + CELL_SIZE // 4, segment[1] + CELL_SIZE // 3),
                                         (segment[0] + CELL_SIZE // 4, segment[1] + 2 * CELL_SIZE // 3)]

                    elif game.snake.direction == (1, 0): #Right
                        eye_positions = [(segment[0] + 2 * CELL_SIZE // 3, segment[1] + CELL_SIZE // 3),
                                         (segment[0] + 2 * CELL_SIZE // 3, segment[1] + 2 * CELL_SIZE // 3)]

                    # Draw the eyes as white rectangles
                    for eye_position in eye_positions:
                        pygame.draw.rect(screen, (255, 255, 255),
                                         (eye_position[0], eye_position[1], CELL_SIZE // 6, CELL_SIZE // 6))

                    # Draw the pupils as black rectangles (in the center of the eyes).
                    for eye_position in eye_positions:
                        pygame.draw.rect(screen, (0, 0, 0), (
                        eye_position[0] + CELL_SIZE // 12, eye_position[1] + CELL_SIZE // 12, CELL_SIZE // 12,
                        CELL_SIZE // 12))
                else:
                    # Draw the rest of the snake segments as you did before.
                    pygame.draw.rect(screen, SNAKE_COLOR, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))

            # Upload food image
            food_image = pygame.image.load(APPLE_IMAGE)

            # Resize image to cell size
            food_image = pygame.transform.scale(food_image, (CELL_SIZE, CELL_SIZE))

            # Draw the resized image in the position of the food.
            screen.blit(food_image, (game.food.position[0], game.food.position[1]))
            current_time = pygame.time.get_ticks()

            # Check if sufficient time has passed since the last update
            if current_time - game.last_update_time >= UPDATE_INTERVAL:

                # Move the snake
                game.snake.move()

                # Check if the head of the snake collides with any segment of the body
                # or if it goes out of the limits of the playing area.
                if any(game.snake.body[0] == segment for segment in game.snake.body[1:]) or (
                        game.snake.body[0][0] < CELL_SIZE
                        or game.snake.body[0][0] >= SCREEN_WIDTH - CELL_SIZE
                        or game.snake.body[0][1] < CELL_SIZE
                        or game.snake.body[0][1] >= SCREEN_HEIGHT - CELL_SIZE
                ):
                    if game.sond:
                        dead_sound.play()
                    game.game_over = True

                # Checking if the snake has eaten an apple
                if game.snake.body[0] == game.food.position:
                    game.snake.grow()
                    game.food_count += 1
                    if game.sond:
                        apple_sound.play()
                    while True:
                        game.food.randomize_position()
                        if all(game.food.position != segment for segment in game.snake.body):
                            break

                game.last_update_time = current_time

        # If the game is finished, we show the death menu.
        if game.game_over:
            save_record(game.food_count)
            time.sleep(0.5)
            restart_game = dead_menu(screen, events,game)  # Llama a la función dead_menu
            if restart_game:
                game.game_over = False
                game.food_count = 0
                game.snake.reset()

        pygame.display.update()


def draw(screen,game):
    """
    Draws the current state of the game on the screen.

    :param screen: The screen area on which the game will be rendered.
    :param game: The instance of the current game that contains the game information.
    :return: None
    """

    # Fills the screen with a white color
    screen.fill((255, 255, 255))

    # Drawing the boxes
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
            if (x // CELL_SIZE + y // CELL_SIZE) % 2 == 0:
                pygame.draw.rect(screen, GRID_COLOR_LIGHT, (x, y, CELL_SIZE, CELL_SIZE))
            else:
                pygame.draw.rect(screen, GRID_COLOR_DARK, (x, y, CELL_SIZE, CELL_SIZE))

    # Drawing the frame of the game
    pygame.draw.rect(screen, FRAME_COLOR, (0, 0, SCREEN_WIDTH, CELL_SIZE))
    pygame.draw.rect(screen, FRAME_COLOR, (0, 0, CELL_SIZE, SCREEN_HEIGHT))
    pygame.draw.rect(screen, FRAME_COLOR, (0, SCREEN_HEIGHT - CELL_SIZE, SCREEN_WIDTH, CELL_SIZE))
    pygame.draw.rect(screen, FRAME_COLOR, (SCREEN_WIDTH - CELL_SIZE, 0, CELL_SIZE, SCREEN_HEIGHT))

    # Draw the apple counter in the upper left corner.
    apple_image = pygame.image.load(APPLE_IMAGE)
    apple_image = pygame.transform.scale(apple_image, (CELL_SIZE-15, CELL_SIZE-15))
    screen.blit(apple_image, (CELL_SIZE, CELL_SIZE // 2 - 13))

    font = pygame.font.Font(None, 24)
    text = font.render(f" : {game.food_count}", True, (255, 255, 255))
    screen.blit(text, (CELL_SIZE + apple_image.get_width(), CELL_SIZE // 2 - 8))

    # Draw record counter in the upper left corner
    trophy_image = pygame.image.load(TROPHY_IMAGE)
    trophy_image = pygame.transform.scale(trophy_image, (CELL_SIZE - 15, CELL_SIZE - 15))
    screen.blit(trophy_image, (CELL_SIZE*3, CELL_SIZE // 2 - 13))

    font = pygame.font.Font(None, 24)
    text = font.render(f" : {get_record()}", True, (255, 255, 255))
    screen.blit(text, ((CELL_SIZE + trophy_image.get_width()*4)+5, CELL_SIZE // 2 - 8))

    # Draw sound button if deactivated or not
    if game.sond:
        sound_image = pygame.image.load(os.path.join("resources/images", "sound_true.png"))
    else:
        sound_image = pygame.image.load(os.path.join("resources/images", "sound_false.png"))

    sound_image = pygame.transform.scale(sound_image, (CELL_SIZE - 15, CELL_SIZE - 15))
    screen.blit(sound_image, (CELL_SIZE * 13 + 10, CELL_SIZE // 2 - 13))


def menu(screen, events):
    """
    Displays the main menu of the game.

    :param screen: The screen area on which the menu will be rendered.
    :param events: A list of pygame events.
    :return: True if the player chooses to start the game, False otherwise.
    """
    # Background color
    screen.fill(GRID_COLOR_LIGHT)

    # Draw the image of an apple in the center of the screen.
    apple_image = pygame.image.load(TROPHY_IMAGE)
    apple_image = pygame.transform.scale(apple_image, (CELL_SIZE * 2, CELL_SIZE * 2))
    apple_rect = apple_image.get_rect()
    apple_rect.center = (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 60)
    screen.blit(apple_image, apple_rect)

    # Draw ":" in the center of the screen.
    font = pygame.font.Font(None, 60)
    colon_text = font.render(":", True, (255, 255, 255))  # Cambio de color a blanco
    colon_rect = colon_text.get_rect()
    colon_rect.center = (SCREEN_WIDTH // 2 + 10, SCREEN_HEIGHT // 2 - 60)
    screen.blit(colon_text, colon_rect)

    # Draw the number of apples that have been eaten.
    font = pygame.font.Font(None, 60)
    points_text = font.render(str(get_record()), True, (255, 255, 255))  # Cambio de color a blanco
    points_rect = points_text.get_rect()
    points_rect.center = (SCREEN_WIDTH // 2 + 50, SCREEN_HEIGHT // 2 - 55)
    screen.blit(points_text, points_rect)

    # Draw the name of the game in the center of the screen.
    font = pygame.font.Font(None, 36)
    text = font.render("Snake Game", True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150)
    screen.blit(text, text_rect)

    # Draw a start button
    button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 50)
    pygame.draw.rect(screen, GRID_COLOR_DARK, button_rect)
    font = pygame.font.Font(None, 24)
    button_text = font.render("Start Game", True, (255, 255, 255))
    button_text_rect = button_text.get_rect()
    button_text_rect.center = button_rect.center
    screen.blit(button_text, button_text_rect)

    # Handle mouse click events
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                return True
    return False


def dead_menu(screen, events, game):
    """
    Displays the game menu when the player loses.

    :param screen: The screen area on which the menu will be rendered.
    :param events: A list of pygame events.
    :param game: The instance of the game with information, such as apple counting.
    :return: True if the player chooses to restart the game, False otherwise.
    """

    # Background color
    screen.fill(GRID_COLOR_LIGHT)

    # Draw the image of an apple in the center of the screen.
    apple_image = pygame.image.load(APPLE_IMAGE)
    apple_image = pygame.transform.scale(apple_image, (CELL_SIZE*2, CELL_SIZE*2))
    apple_rect = apple_image.get_rect()
    apple_rect.center = (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 60)
    screen.blit(apple_image, apple_rect)

    # Draw ":" in the center of the screen.
    font = pygame.font.Font(None, 60)
    colon_text = font.render(":", True, (255, 255, 255))  # Cambio de color a blanco
    colon_rect = colon_text.get_rect()
    colon_rect.center = (SCREEN_WIDTH // 2 + 10, SCREEN_HEIGHT // 2 - 60)
    screen.blit(colon_text, colon_rect)

    # Draw the number of apples that have been eaten.
    font = pygame.font.Font(None, 60)
    points_text = font.render(str(game.food_count), True, (255, 255, 255))  # Cambio de color a blanco
    points_rect = points_text.get_rect()
    points_rect.center = (SCREEN_WIDTH // 2 + 50, SCREEN_HEIGHT // 2 - 55)
    screen.blit(points_text, points_rect)

    # Draw the "Dead" message in the center of the screen.
    font = pygame.font.Font(None, 36)
    text = font.render("You're dead", True, (255, 255, 255))  # Cambio de color a blanco
    text_rect = text.get_rect()
    text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150)
    screen.blit(text, text_rect)

    # Draw a button to restart the game
    button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 50)
    pygame.draw.rect(screen, GRID_COLOR_DARK, button_rect)
    font = pygame.font.Font(None, 24)
    button_text = font.render("Restart Game", True, (255, 255, 255))  # Cambio de color a blanco
    button_text_rect = button_text.get_rect()
    button_text_rect.center = button_rect.center
    screen.blit(button_text, button_text_rect)

    # Handle mouse click events
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                return True  # Si se hace clic en el botón de reiniciar, devuelve True
    return False



if __name__ == "__main__":
    main()
