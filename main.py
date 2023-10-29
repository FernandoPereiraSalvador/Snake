import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE, BLACK, WHITE

# Definir colores
from entities.food import Food
from entities.snake import Snake


def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Game")

    in_menu = True
    game_over = False

    apple_count = 0

    snake = Snake()
    food = Food()

    last_update_time = pygame.time.get_ticks()
    update_interval = 200  # Actualizar cada 100 milisegundos

    while True:
        events = pygame.event.get()  # Obtener eventos en cada iteración

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if in_menu:
                start_game = menu(screen, events)  # Pasa la lista de eventos a la función del menú
                if start_game:
                    in_menu = False

            if game_over:  # Si el juego está en estado "game over"
                restart_game = dead_menu(screen, events)  # Llama a la función dead_menu
                if restart_game:
                    game_over = False
                    apple_count = 0
                    snake.reset()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    snake.change_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    snake.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction((1, 0))
        if not in_menu and not game_over:
            draw(screen, apple_count)
            for segment in snake:
                pygame.draw.rect(screen, (0, 255, 0), (segment[0], segment[1], CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, (255, 0, 0), (food.position[0], food.position[1], CELL_SIZE, CELL_SIZE))
        current_time = pygame.time.get_ticks()
        if current_time - last_update_time >= update_interval:
            snake.move()
            if any(snake.body[0] == segment for segment in snake.body[1:]) or (
                    snake.body[0][0] < CELL_SIZE
                    or snake.body[0][0] >= SCREEN_WIDTH - CELL_SIZE
                    or snake.body[0][1] < CELL_SIZE
                    or snake.body[0][1] >= SCREEN_HEIGHT - CELL_SIZE
            ):
                game_over = True

            if snake.body[0] == food.position:
                snake.grow()
                apple_count += 1
                while True:
                    food.randomize_position()
                    if all(food.position != segment for segment in snake.body):
                        break

            last_update_time = current_time

        pygame.display.update()


def draw(screen, apple_count):
    screen.fill((255, 255, 255))

    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
            if (x // CELL_SIZE + y // CELL_SIZE) % 2 == 0:
                pygame.draw.rect(screen, (0, 0, 0), (x, y, CELL_SIZE, CELL_SIZE))
            else:
                pygame.draw.rect(screen, (255, 255, 255), (x, y, CELL_SIZE, CELL_SIZE))

    # Dibujar el marco del juego
    pygame.draw.rect(screen, BLACK, (0, 0, SCREEN_WIDTH, CELL_SIZE))
    pygame.draw.rect(screen, BLACK, (0, 0, CELL_SIZE, SCREEN_HEIGHT))
    pygame.draw.rect(screen, BLACK, (0, SCREEN_HEIGHT - CELL_SIZE, SCREEN_WIDTH, CELL_SIZE))
    pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH - CELL_SIZE, 0, CELL_SIZE, SCREEN_HEIGHT))

    # Dibujar el contador de manzanas en la esquina superior izquierda
    font = pygame.font.Font(None, 24)
    text = font.render(f"Manzanas: {apple_count}", True, WHITE)
    screen.blit(text, (CELL_SIZE, CELL_SIZE // 2))


def menu(screen, events):
    screen.fill((255, 255, 255))

    # Dibuja el nombre del juego en el centro de la pantalla
    font = pygame.font.Font(None, 36)
    text = font.render("Snake Game", True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
    screen.blit(text, text_rect)

    # Dibuja un botón de inicio
    button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 50)
    pygame.draw.rect(screen, (255, 255, 255), button_rect)
    font = pygame.font.Font(None, 24)
    button_text = font.render("Start Game", True, (0, 0, 0))
    button_text_rect = button_text.get_rect()
    button_text_rect.center = button_rect.center
    screen.blit(button_text, button_text_rect)

    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                return True
    return False


def dead_menu(screen, events):
    screen.fill((255, 255, 255))

    # Dibuja el nombre del juego en el centro de la pantalla
    font = pygame.font.Font(None, 36)
    text = font.render("Snake Game", True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
    screen.blit(text, text_rect)

    # Dibuja el mensaje de "Dead" en el centro de la pantalla
    font = pygame.font.Font(None, 36)
    text = font.render("Dead", True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150)
    screen.blit(text, text_rect)

    # Dibuja un botón para reiniciar el juego
    button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 50)
    pygame.draw.rect(screen, (255, 255, 255), button_rect)
    font = pygame.font.Font(None, 24)
    button_text = font.render("Restart Game", True, (0, 0, 0))
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
