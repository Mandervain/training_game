import pygame, sys, random

# Inicjalizacja Pygame
pygame.init()

# Ustawienia gry
WINDOW_WIDTH, WINDOW_HEIGHT = 300, 600
BLOCK_SIZE = 30
COLUMNS = WINDOW_WIDTH // BLOCK_SIZE
ROWS = WINDOW_HEIGHT // BLOCK_SIZE
FPS = 10

# Kolory
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
WHITE = (255, 255, 255)
COLORS = [
    (0, 255, 255),   # I
    (0, 0, 255),     # J
    (255, 165, 0),   # L
    (255, 255, 0),   # O
    (0, 255, 0),     # S
    (128, 0, 128),   # T
    (255, 0, 0)      # Z
]

# Kształty klocków
SHAPES = [
    [[1, 1, 1, 1]],                         # I
    [[1, 0, 0], [1, 1, 1]],                 # J
    [[0, 0, 1], [1, 1, 1]],                 # L
    [[1, 1], [1, 1]],                       # O
    [[0, 1, 1], [1, 1, 0]],                 # S
    [[0, 1, 0], [1, 1, 1]],                 # T
    [[1, 1, 0], [0, 1, 1]]                  # Z
]

# Ekran
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("🧱 Tetris")

clock = pygame.time.Clock()

# Klasa Tetrimino
class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = random.choice(COLORS)
    
    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

# Funkcje pomocnicze
def create_grid(locked_positions={}):
    grid = [[BLACK for _ in range(COLUMNS)] for _ in range(ROWS)]
    for y in range(ROWS):
        for x in range(COLUMNS):
            if (x, y) in locked_positions:
                grid[y][x] = locked_positions[(x, y)]
    return grid

def valid_space(piece, grid):
    accepted = [[(x, y) for x in range(COLUMNS) if grid[y][x] == BLACK] for y in range(ROWS)]
    accepted = [x for item in accepted for x in item]
    for i, row in enumerate(piece.shape):
        for j, cell in enumerate(row):
            if cell:
                x = piece.x + j
                y = piece.y + i
                if (x, y) not in accepted and y >= 0:
                    return False
    return True

def check_lost(locked_positions):
    for (_, y) in locked_positions:
        if y < 1:
            return True
    return False

def get_shape():
    return Piece(COLUMNS // 2 - 2, 0, random.choice(SHAPES))

def draw_grid_lines(surface):
    for y in range(ROWS):
        pygame.draw.line(surface, GRAY, (0, y * BLOCK_SIZE), (WINDOW_WIDTH, y * BLOCK_SIZE))
    for x in range(COLUMNS):
        pygame.draw.line(surface, GRAY, (x * BLOCK_SIZE, 0), (x * BLOCK_SIZE, WINDOW_HEIGHT))

def clear_rows(grid, locked):
    cleared = 0
    for y in range(ROWS-1, -1, -1):
        if BLACK not in grid[y]:
            cleared += 1
            del_row = y
            for x in range(COLUMNS):
                try:
                    del locked[(x, y)]
                except:
                    continue
    if cleared > 0:
        # Przesuwanie rzędów w dół
        new_locked = {}
        for (x, y), color in locked.items():
            if y < del_row:
                new_locked[(x, y + cleared)] = color
            else:
                new_locked[(x, y)] = color
        locked.clear()
        locked.update(new_locked)
    return cleared

def draw_window(surface, grid, score):
    surface.fill(BLACK)
    for y in range(ROWS):
        for x in range(COLUMNS):
            pygame.draw.rect(surface, grid[y][x],
                             (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
    draw_grid_lines(surface)
    score_text = pygame.font.SysFont(None, 36).render(f"Score: {score}", True, WHITE)
    surface.blit(score_text, (10, 10))
    pygame.display.update()

# Główna funkcja gry
def main():
    locked_positions = {}
    grid = create_grid(locked_positions)
    current_piece = get_shape()
    next_piece = get_shape()
    change_piece = False
    score = 0

    fall_time = 0
    fall_speed = 0.5

    while True:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick(FPS)

        # Opadanie klocka
        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid):
                current_piece.y -= 1
                change_piece = True

        # Obsługa zdarzeń
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                elif event.key == pygame.K_UP:
                    current_piece.rotate()
                    if not valid_space(current_piece, grid):
                        for _ in range(3):  # Obrót cofający
                            current_piece.rotate()

        # Rysowanie aktualnego klocka
        for i, row in enumerate(current_piece.shape):
            for j, cell in enumerate(row):
                if cell:
                    x = current_piece.x + j
                    y = current_piece.y + i
                    if y >= 0:
                        grid[y][x] = current_piece.color

        # Zmiana klocka po dotknięciu dna
        if change_piece:
            for i, row in enumerate(current_piece.shape):
                for j, cell in enumerate(row):
                    if cell:
                        locked_positions[(current_piece.x + j, current_piece.y + i)] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10
            fall_speed = max(0.1, fall_speed - 0.005)  # przyspieszanie gry

        draw_window(screen, grid, score)

        if check_lost(locked_positions):
            pygame.time.wait(2000)
            break

if __name__ == "__main__":
    main()
