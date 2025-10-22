import pygame
import random
import sys

# Inicjalizacja
pygame.init()

# Ustawienia okna
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🍬 Candy Catcher")

# Kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (255, 105, 180)
BLUE = (100, 149, 237)
GREEN = (0, 255, 100)

# Ustawienia gracza
player_size = 50
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT - player_size - 10
player_speed = 7

# Ustawienia cukierków
candy_size = 30
candy_speed = 3
candies = []

# Wynik
score = 0
font = pygame.font.SysFont(None, 36)

# Zegar
clock = pygame.time.Clock()

# Funkcja do tworzenia cukierka
def spawn_candy():
    x = random.randint(0, WIDTH - candy_size)
    y = -candy_size
    candies.append([x, y])

# Główna pętla gry
running = True
spawn_timer = 0

while running:
    clock.tick(60)
    screen.fill(BLUE)

    # Obsługa zdarzeń
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Ruch gracza z przyspieszeniem po wciśnięciu SHIFT
    keys = pygame.key.get_pressed()

    current_speed = player_speed
    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
        current_speed *= 1.8  # zwiększ prędkość o 80%

    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= current_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
        player_x += current_speed


    # Tworzenie nowych cukierków
    spawn_timer += 1
    if spawn_timer > 30:  # co 0.5 sekundy
        spawn_candy()
        spawn_timer = 0

    # Ruch cukierków
    for candy in candies[:]:
        candy[1] += candy_speed
        if candy[1] > HEIGHT:
            candies.remove(candy)
        else:
            # Kolizja z graczem
            if (
                player_x < candy[0] + candy_size and
                player_x + player_size > candy[0] and
                player_y < candy[1] + candy_size and
                player_y + player_size > candy[1]
            ):
                candies.remove(candy)
                score += 1
                candy_speed += 0.1  # gra staje się coraz trudniejsza

    # Rysowanie gracza i cukierków
    pygame.draw.rect(screen, GREEN, (player_x, player_y, player_size, player_size))
    for candy in candies:
        pygame.draw.circle(screen, PINK, (candy[0] + candy_size // 2, candy[1] + candy_size // 2), candy_size // 2)

    # Wyświetlanie wyniku
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))

    # Aktualizacja ekranu
    pygame.display.flip()

# Zakończenie gry
pygame.quit()
sys.exit()
