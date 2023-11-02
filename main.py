import os
import time

import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE, GRID_COLOR_DARK, GRID_COLOR_LIGHT, SNAKE_COLOR, \
    FRAME_COLOR, UPDATE_INTERVAL, BACKGROUND_MUSIC, APPLE_BIT, DEAD_SOUND
from game import Game

from utils.record_utils import get_record, save_record

def main():
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Game")

    game = Game()

    # Iniciar la música
    apple_sound = pygame.mixer.Sound(APPLE_BIT)
    dead_sound = pygame.mixer.Sound(DEAD_SOUND)
    pygame.mixer.music.load(BACKGROUND_MUSIC)
    pygame.mixer.music.play(-1)  # Reproducir la música en un bucle infinito

    while True:
        events = pygame.event.get()  # Obtener eventos en cada iteración

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                pygame.quit()
                return
            if game.in_menu:
                start_game = menu(screen, events)  # Pasa la lista de eventos a la función del menú
                if start_game:
                    game.in_menu = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.snake.change_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    game.snake.change_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    game.snake.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    game.snake.change_direction((1, 0))

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if pygame.Rect(CELL_SIZE * 13 + 10, CELL_SIZE // 2 - 13, CELL_SIZE - 15, CELL_SIZE - 15).collidepoint(event.pos):
                        game.toggle_music()

        if not game.in_menu and not game.game_over:
            draw(screen, game)
            for i, segment in enumerate(game.snake):
                if i == 0:
                    # Dibuja el rectángulo de la cabeza en el color del snake
                    pygame.draw.rect(screen, SNAKE_COLOR, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))

                    # Determina la posición de los ojos en función de la orientación de la cabeza
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

                    # Dibuja los ojos como rectángulos blancos
                    for eye_position in eye_positions:
                        pygame.draw.rect(screen, (255, 255, 255),
                                         (eye_position[0], eye_position[1], CELL_SIZE // 6, CELL_SIZE // 6))

                    # Dibuja las pupilas como rectángulos negros (en el centro de los ojos)
                    for eye_position in eye_positions:
                        pygame.draw.rect(screen, (0, 0, 0), (
                        eye_position[0] + CELL_SIZE // 12, eye_position[1] + CELL_SIZE // 12, CELL_SIZE // 12,
                        CELL_SIZE // 12))
                else:
                    # Dibuja el resto de los segmentos del snake como lo hacías antes
                    pygame.draw.rect(screen, SNAKE_COLOR, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))
            # Cargar la imagen de la comida
            food_image = pygame.image.load(os.path.join("resources/images", "apple.png"))

            # Redimensionar la imagen al tamaño de la celda
            food_image = pygame.transform.scale(food_image, (CELL_SIZE, CELL_SIZE))

            # Dibujar la imagen redimensionada en la posición de la comida
            screen.blit(food_image, (game.food.position[0], game.food.position[1]))
            current_time = pygame.time.get_ticks()
            if current_time - game.last_update_time >= UPDATE_INTERVAL:
                game.snake.move()
                if any(game.snake.body[0] == segment for segment in game.snake.body[1:]) or (
                        game.snake.body[0][0] < CELL_SIZE
                        or game.snake.body[0][0] >= SCREEN_WIDTH - CELL_SIZE
                        or game.snake.body[0][1] < CELL_SIZE
                        or game.snake.body[0][1] >= SCREEN_HEIGHT - CELL_SIZE
                ):
                    if game.sond:
                        dead_sound.play()
                    game.game_over = True

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

        if game.game_over:  # Si el juego está en estado "game over"
            save_record(game.food_count)
            time.sleep(0.5)
            restart_game = dead_menu(screen, events,game)  # Llama a la función dead_menu
            if restart_game:
                game.game_over = False
                game.food_count = 0
                game.snake.reset()

        pygame.display.update()


def draw(screen,game):
    screen.fill((255, 255, 255))

    # Dibujar las casillas
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
            if (x // CELL_SIZE + y // CELL_SIZE) % 2 == 0:
                pygame.draw.rect(screen, GRID_COLOR_LIGHT, (x, y, CELL_SIZE, CELL_SIZE))
            else:
                pygame.draw.rect(screen, GRID_COLOR_DARK, (x, y, CELL_SIZE, CELL_SIZE))

    # Dibujar el marco del juego
    pygame.draw.rect(screen, FRAME_COLOR, (0, 0, SCREEN_WIDTH, CELL_SIZE))
    pygame.draw.rect(screen, FRAME_COLOR, (0, 0, CELL_SIZE, SCREEN_HEIGHT))
    pygame.draw.rect(screen, FRAME_COLOR, (0, SCREEN_HEIGHT - CELL_SIZE, SCREEN_WIDTH, CELL_SIZE))
    pygame.draw.rect(screen, FRAME_COLOR, (SCREEN_WIDTH - CELL_SIZE, 0, CELL_SIZE, SCREEN_HEIGHT))

    # Dibujar el contador de manzanas en la esquina superior izquierda
    apple_image = pygame.image.load(os.path.join("resources/images", "apple.png"))
    apple_image = pygame.transform.scale(apple_image, (CELL_SIZE-15, CELL_SIZE-15))
    screen.blit(apple_image, (CELL_SIZE, CELL_SIZE // 2 - 13))

    font = pygame.font.Font(None, 24)
    text = font.render(f" : {game.food_count}", True, (255, 255, 255))
    screen.blit(text, (CELL_SIZE + apple_image.get_width(), CELL_SIZE // 2 - 8))

    # Dibujar el contador de records en la esquina superior izquierda
    trophy_image = pygame.image.load(os.path.join("resources/images", "trophy.png"))
    trophy_image = pygame.transform.scale(trophy_image, (CELL_SIZE - 15, CELL_SIZE - 15))
    screen.blit(trophy_image, (CELL_SIZE*3, CELL_SIZE // 2 - 13))

    font = pygame.font.Font(None, 24)
    text = font.render(f" : {get_record()}", True, (255, 255, 255))
    screen.blit(text, ((CELL_SIZE + trophy_image.get_width()*4)+5, CELL_SIZE // 2 - 8))

    # Dibujar el contador de records en la esquina superior izquierda
    trophy_image = pygame.image.load(os.path.join("resources/images", "trophy.png"))
    trophy_image = pygame.transform.scale(trophy_image, (CELL_SIZE - 15, CELL_SIZE - 15))
    screen.blit(trophy_image, (CELL_SIZE * 3, CELL_SIZE // 2 - 13))

    font = pygame.font.Font(None, 24)
    text = font.render(f" : {get_record()}", True, (255, 255, 255))
    screen.blit(text, ((CELL_SIZE + trophy_image.get_width() * 4) + 5, CELL_SIZE // 2 - 8))

    # Dibujar boton sonido
    if game.sond:
        sound_image = pygame.image.load(os.path.join("resources/images", "sound_true.png"))
    else:
        sound_image = pygame.image.load(os.path.join("resources/images", "sound_false.png"))

    sound_image = pygame.transform.scale(sound_image, (CELL_SIZE - 15, CELL_SIZE - 15))
    screen.blit(sound_image, (CELL_SIZE * 13 + 10, CELL_SIZE // 2 - 13))


def menu(screen, events):
    screen.fill(GRID_COLOR_LIGHT)

    # Dibuja la imagen de una manzana en el centro de la pantalla
    apple_image = pygame.image.load(os.path.join("resources/images", "trophy.png"))
    apple_image = pygame.transform.scale(apple_image, (CELL_SIZE * 2, CELL_SIZE * 2))
    apple_rect = apple_image.get_rect()
    apple_rect.center = (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 60)
    screen.blit(apple_image, apple_rect)

    # Dibuja ":" en el centro de la pantalla
    font = pygame.font.Font(None, 60)
    colon_text = font.render(":", True, (255, 255, 255))  # Cambio de color a blanco
    colon_rect = colon_text.get_rect()
    colon_rect.center = (SCREEN_WIDTH // 2 + 10, SCREEN_HEIGHT // 2 - 60)
    screen.blit(colon_text, colon_rect)

    # Dibuja el número de manzanas que se han comido
    font = pygame.font.Font(None, 60)
    points_text = font.render(str(get_record()), True, (255, 255, 255))  # Cambio de color a blanco
    points_rect = points_text.get_rect()
    points_rect.center = (SCREEN_WIDTH // 2 + 50, SCREEN_HEIGHT // 2 - 55)
    screen.blit(points_text, points_rect)

    # Dibuja el nombre del juego en el centro de la pantalla
    font = pygame.font.Font(None, 36)
    text = font.render("Snake Game", True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150)
    screen.blit(text, text_rect)

    # Dibuja un botón de inicio
    button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 50)
    pygame.draw.rect(screen, GRID_COLOR_DARK, button_rect)
    font = pygame.font.Font(None, 24)
    button_text = font.render("Start Game", True, (255, 255, 255))
    button_text_rect = button_text.get_rect()
    button_text_rect.center = button_rect.center
    screen.blit(button_text, button_text_rect)

    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                return True
    return False


def dead_menu(screen, events, game):
    screen.fill(GRID_COLOR_LIGHT)

    # Dibuja la imagen de una manzana en el centro de la pantalla
    apple_image = pygame.image.load(os.path.join("resources/images", "apple.png"))
    apple_image = pygame.transform.scale(apple_image, (CELL_SIZE*2, CELL_SIZE*2))
    apple_rect = apple_image.get_rect()
    apple_rect.center = (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 60)
    screen.blit(apple_image, apple_rect)

    # Dibuja ":" en el centro de la pantalla
    font = pygame.font.Font(None, 60)
    colon_text = font.render(":", True, (255, 255, 255))  # Cambio de color a blanco
    colon_rect = colon_text.get_rect()
    colon_rect.center = (SCREEN_WIDTH // 2 + 10, SCREEN_HEIGHT // 2 - 60)
    screen.blit(colon_text, colon_rect)

    # Dibuja el número de manzanas que se han comido
    font = pygame.font.Font(None, 60)
    points_text = font.render(str(game.food_count), True, (255, 255, 255))  # Cambio de color a blanco
    points_rect = points_text.get_rect()
    points_rect.center = (SCREEN_WIDTH // 2 + 50, SCREEN_HEIGHT // 2 - 55)
    screen.blit(points_text, points_rect)

    # Dibuja el mensaje de "Dead" en el centro de la pantalla
    font = pygame.font.Font(None, 36)
    text = font.render("You're dead", True, (255, 255, 255))  # Cambio de color a blanco
    text_rect = text.get_rect()
    text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150)
    screen.blit(text, text_rect)

    # Dibuja un botón para reiniciar el juego
    button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 50)
    pygame.draw.rect(screen, GRID_COLOR_DARK, button_rect)
    font = pygame.font.Font(None, 24)
    button_text = font.render("Restart Game", True, (255, 255, 255))  # Cambio de color a blanco
    button_text_rect = button_text.get_rect()
    button_text_rect.center = button_rect.center
    screen.blit(button_text, button_text_rect)

    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                return True  # Si se hace clic en el botón de reiniciar, devuelve True
    return False



if __name__ == "__main__":
    main()
