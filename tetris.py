import pygame
import random

# Initialize the pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 300, 600
CELL_SIZE = 30
COLUMNS, ROWS = SCREEN_WIDTH // CELL_SIZE, SCREEN_HEIGHT // CELL_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [
    (0, 255, 255),  # Cyan
    (255, 165, 0),  # Orange
    (0, 0, 255),  # Blue
    (255, 255, 0),  # Yellow
    (0, 255, 0),  # Green
    (255, 0, 0),  # Red
    (128, 0, 128),  # Purple
]

# Tetrimino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1], [1, 1]],  # O
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
]


class Tetrimino:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = random.choice(COLORS)
        self.x = COLUMNS // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]


def check_collision(board, shape, offset):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell and (
                x + off_x < 0
                or x + off_x >= COLUMNS
                or y + off_y >= ROWS
                or board[y + off_y][x + off_x]
            ):
                return True
    return False


def remove_full_lines(board):
    new_board = [row for row in board if any(cell == 0 for cell in row)]
    lines_cleared = ROWS - len(new_board)
    new_board = [[0 for _ in range(COLUMNS)] for _ in range(lines_cleared)] + new_board
    return new_board, lines_cleared


def draw_board(screen, board, tetrimino):
    screen.fill(BLACK)
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(
                    screen,
                    cell,
                    pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                )
    for y, row in enumerate(tetrimino.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(
                    screen,
                    tetrimino.color,
                    pygame.Rect(
                        (tetrimino.x + x) * CELL_SIZE,
                        (tetrimino.y + y) * CELL_SIZE,
                        CELL_SIZE,
                        CELL_SIZE,
                    ),
                )
    pygame.display.update()


def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    board = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]
    tetrimino = Tetrimino()
    game_over = False
    speed = 500
    last_fall_time = pygame.time.get_ticks()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if not check_collision(
                        board, tetrimino.shape, (tetrimino.x - 1, tetrimino.y)
                    ):
                        tetrimino.x -= 1
                elif event.key == pygame.K_RIGHT:
                    if not check_collision(
                        board, tetrimino.shape, (tetrimino.x + 1, tetrimino.y)
                    ):
                        tetrimino.x += 1
                elif event.key == pygame.K_DOWN:
                    if not check_collision(
                        board, tetrimino.shape, (tetrimino.x, tetrimino.y + 1)
                    ):
                        tetrimino.y += 1
                elif event.key == pygame.K_UP:
                    tetrimino.rotate()
                    if check_collision(
                        board, tetrimino.shape, (tetrimino.x, tetrimino.y)
                    ):
                        tetrimino.rotate()
                        tetrimino.rotate()
                        tetrimino.rotate()

        if pygame.time.get_ticks() - last_fall_time > speed:
            if not check_collision(
                board, tetrimino.shape, (tetrimino.x, tetrimino.y + 1)
            ):
                tetrimino.y += 1
            else:
                for y, row in enumerate(tetrimino.shape):
                    for x, cell in enumerate(row):
                        if cell:
                            board[y + tetrimino.y][x + tetrimino.x] = tetrimino.color
                board, lines_cleared = remove_full_lines(board)
                tetrimino = Tetrimino()
                if check_collision(board, tetrimino.shape, (tetrimino.x, tetrimino.y)):
                    game_over = True
            last_fall_time = pygame.time.get_ticks()

        draw_board(screen, board, tetrimino)
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
