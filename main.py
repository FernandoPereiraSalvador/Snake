import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE

# Definir colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Game")

    in_menu = True
    events = []  # Lista para almacenar eventos

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
        if not in_menu:
            draw(screen)
        pygame.display.update()

def draw(screen):
    screen.fill((255, 255, 255))

    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
            if (x // CELL_SIZE + y // CELL_SIZE) % 2 == 0:
                pygame.draw.rect(screen, (0, 0, 0), (x, y, CELL_SIZE, CELL_SIZE))
            else:
                pygame.draw.rect(screen, (255, 255, 255), (x, y, CELL_SIZE, CELL_SIZE))

def menu(screen, events):
    screen.fill((255, 255, 255))

    # Dibuja el nombre del juego en el centro de la pantalla
    font = pygame.font.Font(None, 36)
    text = font.render("Snake Game", True, (0,0,0))
    text_rect = text.get_rect()
    text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
    screen.blit(text, text_rect)

    # Dibuja un botón de inicio
    button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 50)
    pygame.draw.rect(screen, (255,255,255), button_rect)
    font = pygame.font.Font(None, 24)
    button_text = font.render("Start Game", True, (0,0,0))
    button_text_rect = button_text.get_rect()
    button_text_rect.center = button_rect.center
    screen.blit(button_text, button_text_rect)

    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                return True
    return False

if __name__ == "__main__":
    main()
