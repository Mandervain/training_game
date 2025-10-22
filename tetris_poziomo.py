import pygame, sys, random

pygame.init()

# --- Ustawienia gry ---
BLOCK_SIZE = 30
ROWS = 10
COLUMNS = 20
WIDTH = COLUMNS * BLOCK_SIZE
HEIGHT = ROWS * BLOCK_SIZE
FPS = 30

# --- Kolory ---
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

# --- Kształty ---
SHAPES = [
    [[1, 1, 1, 1]],                         # I
    [[1, 0, 0], [1, 1, 1]],                 # J
    [[0, 0, 1], [1, 1, 1]],                 # L
    [[1, 1], [1, 1]],                       # O
    [[0, 1, 1], [1, 1, 0]],                 # S
    [[0, 1, 0], [1, 1, 1]],                 # T
    [[1, 1, 0], [0, 1, 1]]                  # Z
]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("⬅️ Sideways Tetris")

clock = pygame.time.Clock()


# --- Klasa klocka ---
class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = random.choice(COLORS)

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]


# --- Tworzenie planszy ---
def create_grid(locked_positions):
    grid = [[BLACK for _ in range(COLUMNS)] for _ in range(ROWS)]
    for (x, y), color in locked_positions.items():
        if 0 <= x < COLUMNS and 0 <= y < ROWS:
            grid[y][x] = color
    return grid


# --- Sprawdzenie kolizji ---
def valid_space(piece, grid):
    for i, row in enumerate(piece.shape):
        for j, cell in enumerate(row):
            if cell:
                new_x = piece.x + j
                new_y = piece.y + i
                if new_x < 0 or new_x >= COLUMNS or new_y < 0 or new_y >= ROWS:
                    return False
                if grid[new_y][new_x] != BLACK:
                    return False
    return True


# --- Sprawdzenie przegranej ---
def check_lost(locked_positions):
    for (x, y) in locked_positions:
        if x >= COLUMNS - 1:
            return True
    return False


# --- Losowanie nowego klocka ---
def get_shape():
    shape = random.choice(SHAPES)
    start_x = COLUMNS - len(shape[0])  # start po prawej stronie
    start_y = ROWS // 2 - len(shape) // 2
    return Piece(start_x, start_y, shape)


# --- Czyszczenie pełnych kolumn ---
def clear_columns(grid, locked):
    cleared = 0
    for x in range(COLUMNS):
        if all(grid[y][x] != BLACK for y in range(ROWS)):
            cleared += 1
            for y in range(ROWS):
                if (x, y) in locked:
                    del locked[(x, y)]
            # przesuwamy wszystko z prawej w lewo
            new_locked = {}
            for (lx, ly), color in locked.items():
                if lx > x:
                    new_locked[(lx - 1, ly)] = color
                else:
                    new_locked[(lx, ly)] = color
            locked.clear()
            locked.update(new_locked)
    return cleared


# --- Rysowanie ---
def draw_grid(surface):
    for y in range(ROWS):
        pygame.draw.line(surface, GRAY, (0, y * BLOCK_SIZE), (WIDTH, y * BLOCK_SIZE))
    for x in range(COLUMNS):
        pygame.draw.line(surface, GRAY, (x * BLOCK_SIZE, 0), (x * BLOCK_SIZE, HEIGHT))


def draw_window(surface, grid, score):
    surface.fill(BLACK)
    for y in range(ROWS):
        for x in range(COLUMNS):
            pygame.draw.rect(surface, grid[y][x],
                             (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    draw_grid(surface)
    font = pygame.font.SysFont(None, 32)
    score_text = font.render(f"Score: {score}", True, WHITE)
    surface.blit(score_text, (10, 10))
    pygame.display.update()


# --- Hard drop ---
def hard_drop(piece, grid):
    while True:
        piece.x -= 1
        if not valid_space(piece, grid):
            piece.x += 1
            break


# --- Główna pętla gry ---
def main():
    locked_positions = {}
    current_piece = get_shape()
    next_piece = get_shape()
    fall_time = 0
    fall_speed = 0.5
    score = 0
    change_piece = False

    while True:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick(FPS)

        # automatyczny ruch w lewo
        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.x -= 1
            if not valid_space(current_piece, grid):
                current_piece.x += 1
                change_piece = True

        # obsługa sterowania
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                    # obrót
                    current_piece.rotate()
                    if not valid_space(current_piece, grid):
                        for _ in range(3):
                            current_piece.rotate()
                elif event.key == pygame.K_LEFT:
                    # przesunięcie w dół
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                elif event.key == pygame.K_RIGHT:
                    # przesunięcie w górę
                    current_piece.y -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.y += 1
                elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    # natychmiastowy drop
                    hard_drop(current_piece, grid)
                    change_piece = True

        # narysuj klocek
        for i, row in enumerate(current_piece.shape):
            for j, cell in enumerate(row):
                if cell:
                    x = current_piece.x + j
                    y = current_piece.y + i
                    if 0 <= x < COLUMNS and 0 <= y < ROWS:
                        grid[y][x] = current_piece.color

        # nowy klocek po kolizji
        if change_piece:
            for i, row in enumerate(current_piece.shape):
                for j, cell in enumerate(row):
                    if cell:
                        locked_positions[(current_piece.x + j, current_piece.y + i)] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_columns(grid, locked_positions) * 10
            fall_speed = max(0.1, fall_speed - 0.01)

        draw_window(screen, grid, score)

        if check_lost(locked_positions):
            pygame.time.wait(2000)
            break


if __name__ == "__main__":
    main()
