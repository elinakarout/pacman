import pygame
from collections import deque
from typing import Literal
from dataclasses import dataclass, field
from .player import DIRECTIONS, ANGLES


EDIBLE_DURATION = 8.0
OPPOSITE = {"up": "down", "down": "up", "left": "right", "right": "left"}


@dataclass
class Ghost:
    name: Literal["INKY", "PINKY", "BLINKY", "CLYDE"]
    home_col: int
    home_row: int
    start_delay: int
    col: int
    row: int
    asset: str
    speed: float
    state: Literal["wait", "chase", "edible", "eaten"]
    images: dict[str, pygame.Surface] = field(default_factory=dict)
    direction: str | None = None
    timer: float = 0.0
    wait_time: float = 0.0
    edible_time: float = 0.0

    def draw(
        self, surface: pygame.Surface,
        origin: tuple[int, int], cell_size: int
    ) -> None:
        img = self.images["right"]
        x = (
            origin[0] + self.col * cell_size
            + (cell_size - img.get_width()) // 2
        )
        y = (
            origin[1] + self.row * cell_size
            + (cell_size - img.get_height()) // 2
        )
        surface.blit(img, (x, y))

    def make_edible(self) -> None:
        if self.state in ("chase", "edible"):
            self.state = "edible"
            self.edible_time = 0.0

    def reset(self, speed: float) -> None:
        self.col = self.home_col
        self.row = self.home_row
        self.state = "wait"
        self.direction = None
        self.timer = 0.0
        self.wait_time = 0.0
        self.edible_time = 0.0
        self.speed = speed

    def open_directions(self, maze: list[list[int]]) -> list[str]:
        options = [
            name for name, (_, _, bit) in DIRECTIONS.items()
            if not maze[self.row][self.col] & bit
        ]
        if self.direction and len(options) > 1:
            options = [d for d in options if d != OPPOSITE[self.direction]]
        return options

    def chase_target(
        self, player: tuple[int, int], player_dir: str,
        blinky: tuple[int, int]
    ) -> tuple[int, int]:
        p_col, p_row = player
        d_row, d_col, _ = DIRECTIONS[player_dir]
        if self.name == "BLINKY":
            return player
        if self.name == "PINKY":
            offset_col = -4 if player_dir == "up" else 4 * d_col
            return (p_col + offset_col, p_row + 4 * d_row)
        if self.name == "INKY":
            ahead = (p_col + 2 * d_col, p_row + 2 * d_row)
            return (2 * ahead[0] - blinky[0], 2 * ahead[1] - blinky[1])
        dx, dy = self.col - p_col, self.row - p_row
        if dx * dx + dy * dy > 64:
            return player
        return (self.home_col, self.home_row)

    def bfs(
        self, maze: list[list[int]], start: tuple[int, int]
    ) -> dict[tuple[int, int], tuple[int, str | None]]:
        """Path length from start to every reachable cell, plus the first
        direction to take from start to get there."""
        rows, cols = len(maze), len(maze[0])
        seen: dict[tuple[int, int], tuple[int, str | None]] = {
            start: (0, None)
        }
        queue = deque([start])
        while queue:
            col, row = queue.popleft()
            dist, first = seen[(col, row)]
            for name, (d_row, d_col, bit) in DIRECTIONS.items():
                if maze[row][col] & bit:
                    continue
                nxt = (col + d_col, row + d_row)
                if nxt in seen or not (
                    0 <= nxt[0] < cols and 0 <= nxt[1] < rows
                ):
                    continue
                seen[nxt] = (dist + 1, first or name)
                queue.append(nxt)
        return seen

    def choose_direction(
        self, maze: list[list[int]], options: list[str],
        target: tuple[int, int], player: tuple[int, int]
    ) -> str:
        if self.state == "edible":
            from_player = self.bfs(maze, player)

            def flee(name: str) -> int:
                d_row, d_col, _ = DIRECTIONS[name]
                cell = (self.col + d_col, self.row + d_row)
                return from_player.get(cell, (0, None))[0]
            return max(options, key=flee)
        paths = self.bfs(maze, (self.col, self.row))
        goal = min(
            (cell for cell in paths if cell != (self.col, self.row)),
            key=lambda c: (
                abs(c[0] - target[0]) + abs(c[1] - target[1]), paths[c][0]
            ),
            default=None,
        )
        if goal is not None:
            first = paths[goal][1]
            if first in options:
                return first
        return options[0]

    def update(
        self, dt: float, maze: list[list[int]],
        player: tuple[int, int], player_dir: str,
        blinky: tuple[int, int]
    ) -> None:
        if self.state == "wait":
            self.wait_time += dt
            if self.wait_time >= self.start_delay:
                self.state = "chase"
            return
        if self.state == "eaten":
            return
        if self.state == "edible":
            self.edible_time += dt
            if self.edible_time >= EDIBLE_DURATION:
                self.state = "chase"
        self.timer += dt
        if self.timer < 1 / self.speed:
            return
        self.timer = 0
        if self.state == "chase":
            target = self.chase_target(player, player_dir, blinky)
        else:
            target = player
        options = self.open_directions(maze)
        if not options:
            return
        self.direction = self.choose_direction(maze, options, target, player)
        d_row, d_col, _ = DIRECTIONS[self.direction]
        self.row += d_row
        self.col += d_col


class Ghosts:
    def __init__(
        self, maze: list[list[int]],
        cell_size: int, speed: int = 3
    ) -> None:
        self.maze = maze
        self.cell_size = cell_size
        self.speed = speed
        self.ghosts = self.spawn_ghosts()

    def spawn_ghosts(self) -> list[Ghost]:
        cols = len(self.maze[0])
        rows = len(self.maze)
        ghosts: list[Ghost] = []
        ghosts.append(Ghost(
            name="BLINKY",
            home_col=1,
            home_row=0,
            start_delay=3,
            col=1,
            row=0,
            asset=("assets/blinky.png"),
            speed=self.speed,
            state="wait"
        ))
        ghosts.append(Ghost(
            name="PINKY",
            home_col=1,
            home_row=rows - 1,
            start_delay=6,
            col=1,
            row=rows - 1,
            asset=("assets/pinky.png"),
            speed=self.speed,
            state="wait"
        ))
        ghosts.append(Ghost(
            name="INKY",
            home_col=cols - 2,
            home_row=rows - 1,
            start_delay=9,
            col=cols - 2,
            row=rows - 1,
            asset=("assets/inky.png"),
            speed=self.speed,
            state="wait"
        ))
        ghosts.append(Ghost(
            name="CLYDE",
            home_col=cols - 2,
            home_row=0,
            start_delay=12,
            col=cols - 2,
            row=0,
            asset=("assets/clyde.png"),
            speed=self.speed,
            state="wait"
        ))
        size = self.cell_size - 8
        for ghost in ghosts:
            base = pygame.image.load(ghost.asset).convert_alpha()
            base_image = pygame.transform.smoothscale(base, (size, size))
            ghost.images = {
                name: pygame.transform.rotate(base_image, angle)
                for name, angle in ANGLES.items()
            }
        return ghosts

    def update(
        self, dt: float, player: tuple[int, int], player_dir: str,
        dots_left: float
    ) -> None:
        blinky = next(g for g in self.ghosts if g.name == "BLINKY")
        if dots_left < 0.15:
            blinky.speed = self.speed * 1.4
        elif dots_left < 0.30:
            blinky.speed = self.speed * 1.2
        for ghost in self.ghosts:
            ghost.update(
                dt, self.maze, player, player_dir, (blinky.col, blinky.row)
            )

    def draw(self, surface: pygame.Surface, origin: tuple[int, int]) -> None:
        for ghost in self.ghosts:
            ghost.draw(surface, origin, self.cell_size)

    def collide(self, position: tuple[int, int]) -> tuple[bool, bool]:
        row, col = position
        killed = False
        ate = False
        for ghost in self.ghosts:
            if ghost.row != row or ghost.col != col:
                continue
            if ghost.state == "edible":
                ghost.reset(self.speed)
                ate = True
            elif ghost.state != "eaten":
                killed = True
        return killed, ate
