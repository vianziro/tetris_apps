

import pygame
import random
import time

pygame.init()
pygame.mixer.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
SCREEN_WIDTH = BLOCK_SIZE * (GRID_WIDTH + 6)
SCREEN_HEIGHT = BLOCK_SIZE * GRID_HEIGHT

SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
]

COLORS = [CYAN, YELLOW, MAGENTA, ORANGE, BLUE, GREEN, RED]

class Tetris:
    def __init__(self):
        """Inisialisasi game Tetris dengan pengaturan awal."""
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.start_time = time.time()
        self.elapsed_time = 0
        self.base_fall_speed = 500
        self.current_fall_speed = self.base_fall_speed
        self.reset_game()

    def reset_game(self):
        """Mengatur ulang permainan ke kondisi awal."""
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.game_over = False
        self.score = 0

    def new_piece(self):
        """Membuat tetromino baru dengan bentuk dan warna acak."""
        shape = random.choice(SHAPES)
        color = COLORS[SHAPES.index(shape)]
        return {
            "shape": shape,
            "color": color,
            "x": GRID_WIDTH // 2 - len(shape[0]) // 2,
            "y": 0,
        }

    def valid_move(self, piece, x, y):
        """Memeriksa apakah pergerakan tetromino valid."""
        for i, row in enumerate(piece["shape"]):
            for j, cell in enumerate(row):
                if cell:
                    new_x = piece["x"] + j + x
                    new_y = piece["y"] + i + y
                    if (
                        new_x < 0
                        or new_x >= GRID_WIDTH
                        or new_y >= GRID_HEIGHT
                        or (new_y >= 0 and self.grid[new_y][new_x])
                    ):
                        return False
        return True

    def rotate_piece(self, piece):
        """Memutar tetromino searah jarum jam."""
        rotated = list(zip(*piece["shape"][::-1]))
        if self.valid_move({"shape": rotated, "x": piece["x"], "y": piece["y"]}, 0, 0):
            piece["shape"] = rotated

    def place_piece(self):
        """Menempatkan tetromino pada grid permainan."""
        for i, row in enumerate(self.current_piece["shape"]):
            for j, cell in enumerate(row):
                if cell:
                    self.grid[self.current_piece["y"] + i][
                        self.current_piece["x"] + j
                    ] = self.current_piece["color"]

    def clear_lines(self):
        """Menghapus baris yang terisi penuh dan menambah skor."""
        lines_cleared = 0
        i = GRID_HEIGHT - 1
        while i >= 0:
            if all(self.grid[i]):
                del self.grid[i]
                self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])
                lines_cleared += 1
            else:
                i -= 1
        if lines_cleared > 0:
            self.score += (2 ** (lines_cleared - 1)) * 100
            self.current_fall_speed = max(100, self.base_fall_speed - (self.score // 1000) * 50)

    def draw(self):
        """Menggambar seluruh elemen permainan ke layar."""
        self.screen.fill(BLACK)
        
        self.elapsed_time = int(time.time() - self.start_time)

        for i in range(GRID_HEIGHT):
            for j in range(GRID_WIDTH):
                pygame.draw.rect(
                    self.screen,
                    WHITE,
                    [j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE],
                    1,
                )
                if self.grid[i][j]:
                    pygame.draw.rect(
                        self.screen,
                        self.grid[i][j],
                        [
                            j * BLOCK_SIZE,
                            i * BLOCK_SIZE,
                            BLOCK_SIZE - 1,
                            BLOCK_SIZE - 1,
                        ],
                    )

        if self.current_piece:
            for i, row in enumerate(self.current_piece["shape"]):
                for j, cell in enumerate(row):
                    if cell:
                        pygame.draw.rect(
                            self.screen,
                            self.current_piece["color"],
                            [
                                (self.current_piece["x"] + j) * BLOCK_SIZE,
                                (self.current_piece["y"] + i) * BLOCK_SIZE,
                                BLOCK_SIZE - 1,
                                BLOCK_SIZE - 1,
                            ],
                        )

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, [GRID_WIDTH * BLOCK_SIZE + 10, 10])
        
        minutes = self.elapsed_time // 60
        seconds = self.elapsed_time % 60
        time_text = font.render(f"Time: {minutes:02d}:{seconds:02d}", True, WHITE)
        self.screen.blit(time_text, [GRID_WIDTH * BLOCK_SIZE + 10, 50])

        pygame.display.flip()

    def run(self):
        """Menjalankan loop utama permainan."""
        fall_time = 0
        try:
            pygame.mixer.music.load("tetris_theme.mp3")
            pygame.mixer.music.play(-1)
        except:
            print("Could not load background music")

        while not self.game_over:
            fall_time += self.clock.get_rawtime()
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if self.valid_move(self.current_piece, -1, 0):
                            self.current_piece["x"] -= 1
                    if event.key == pygame.K_RIGHT:
                        if self.valid_move(self.current_piece, 1, 0):
                            self.current_piece["x"] += 1
                    if event.key == pygame.K_DOWN:
                        if self.valid_move(self.current_piece, 0, 1):
                            self.current_piece["y"] += 1
                    if event.key == pygame.K_UP:
                        self.rotate_piece(self.current_piece)

            if fall_time >= self.current_fall_speed:
                if self.valid_move(self.current_piece, 0, 1):
                    self.current_piece["y"] += 1
                else:
                    self.place_piece()
                    self.clear_lines()
                    self.current_piece = self.new_piece()
                    if not self.valid_move(self.current_piece, 0, 0):
                        self.game_over = True
                fall_time = 0

            self.draw()

        font = pygame.font.Font(None, 48)
        game_over_text = font.render("Game Over!", True, WHITE)
        self.screen.blit(game_over_text, [SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2])
        pygame.display.flip()
        pygame.time.wait(2000)


if __name__ == "__main__":
    game = Tetris()
    game.run()
    pygame.quit()
