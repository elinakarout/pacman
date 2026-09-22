import pygame
from typing import Union
from ..config.data import CHEATS

# (row, col, wall bit)
DIRECTIONS = {
    "up": (-1, 0, 1),
    "right": (0, 1, 2),
    "down": (1, 0, 4),
    "left": (0, -1, 8),
}


ANGLES = {"down": 0, "right": 90, "up": 180, "left": 270}


class Player:
    def __init__(
        self, maze: list[list[int]], lives: int,
        cell_size: int, speed: float = 4,

    ) -> None:
        self.player_size = cell_size - 8
        self.timer = 0.0
        self.facing = "right"
        self.change_skin("pacraft_assets/Steve_front.png")
        self.maze = maze
        self.row, self.col = self.get_start(maze)
        self.lives = lives
        self.score = 0
        self.speed = speed
        self.direction: Union[str, None] = None
        self.next_direction: Union[str, None] = None

    @staticmethod
    def get_start(maze: list[list[int]]) -> tuple[int, int]:
        y = len(maze) // 2
        x = len(maze[0]) // 2
        while maze[y][x] == 15:
            x += 1
        return (y, x)

    def change_skin(self, new_image_path: str) -> None:
        size = self.player_size
        base = pygame.image.load(new_image_path).convert_alpha()
        base_image = pygame.transform.smoothscale(base, (size, size))
        self.images = {
            name: pygame.transform.rotate(base_image, angle)
            for name, angle in ANGLES.items()
        }

    def can_move(self, direction: str) -> bool:
        _, _, bit = DIRECTIONS[direction]
        return not (self.maze[self.row][self.col] & bit)

    def handle_key(self, key: int) -> None:
        keys = {
            pygame.K_UP: "up", pygame.K_w: "up",
            pygame.K_DOWN: "down", pygame.K_s: "down",
            pygame.K_LEFT: "left", pygame.K_a: "left",
            pygame.K_RIGHT: "right", pygame.K_d: "right"
        }
        if key in keys:
            self.next_direction = keys[key]

    def move(self, direction: str) -> None:
        self.facing = direction
        if self.can_move(direction):
            d_row, d_col, _ = DIRECTIONS[direction]
            self.row += d_row
            self.col += d_col

    def increase_speed(self) -> None:
        if self.speed > 6:
            return
        self.speed += 0.5

    def update(self, dt: float) -> None:
        self.timer += dt
        if self.timer < 1 / self.speed:
            return
        self.timer = 0
        if self.next_direction and self.can_move(self.next_direction):
            self.direction = self.next_direction
        if self.direction and self.can_move(self.direction):
            d_row, d_col, _ = DIRECTIONS[self.direction]
            self.row += d_row
            self.col += d_col
            self.facing = self.direction
        else:
            self.direction = None

    def draw(self, surface: pygame.Surface, origin: tuple[int, int],
             cell_size: int) -> None:
        if CHEATS["cheater"]:
            self.change_skin("pacraft_assets/Chicken.png")
        img = self.images[self.facing]
        x = (
            origin[0] + self.col * cell_size
            + (cell_size - img.get_width()) // 2
        )
        y = (
            origin[1] + self.row * cell_size
            + (cell_size - img.get_height()) // 2
        )
        surface.blit(img, (x, y))
