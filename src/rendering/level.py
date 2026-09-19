from typing import Tuple
import pygame
from mazegenerator import MazeGenerator
from src.config import Config
from src.entities import Player


class Level(pygame.Surface):
    def __init__(
        self, configs: Config, size: Tuple[int, int]
    ) -> None:
        self.CELL_SIZE = 50
        self.levels = configs.levels
        self.current_level = 1
        self.current_width = self.levels[self.current_level - 1].width
        self.current_height = self.levels[self.current_level - 1].height
        self.maze_size = (self.current_width, self.current_height)
        self.maze = MazeGenerator(self.maze_size).maze
        self.WALL_COLOR = (255, 255, 255)
        self.lives = configs.lives
        self.points_per_pacgum = configs.points_per_pacgum
        self.points_per_super_pacgum = configs.points_per_super_pacgum
        self.font = pygame.font.Font(None, 40)
        super().__init__(size)

    def get_center(self, width: int, height: int) -> Tuple[int, int]:
        s_width, s_height = self.get_size()
        m_width = width * self.CELL_SIZE
        m_height = height * self.CELL_SIZE
        center = ((s_width - m_width) // 2,
                  (s_height - m_height) // 2)
        return center

    def draw_wall_at(
        self, start: Tuple[int, int], end: Tuple[int, int]
    ) -> None:
        pygame.draw.line(
            self, (255, 255, 255), start, end, 1
        )

    def draw_pacgums(self) -> None:
        half = self.CELL_SIZE // 2
        for row, col in self.pacgums:
            x = self.center[0] + col * self.CELL_SIZE + half
            y = self.center[1] + row * self.CELL_SIZE + half
            pygame.draw.circle(self, (255, 200, 150), (x, y), 4)
        for row, col in self.super_pacgums:
            x = self.center[0] + col * self.CELL_SIZE + half
            y = self.center[1] + row * self.CELL_SIZE + half
            pygame.draw.circle(self, (255, 200, 150), (x, y), 8)

    def draw_score(self) -> None:
        margin = 20
        width = self.get_width()
        score = self.font.render(
            f"SCORE: {self.player.score}", True, (255, 255, 255)
        )
        self.blit(score, (width - score.get_width() - margin, margin))
        lives = self.font.render(
            f"LIVES: {self.player.lives}", True, (255, 255, 255)
        )
        self.blit(lives, (margin, margin))

    def setup(self) -> None:
        self.fill((0, 0, 0))
        center = self.get_center(self.maze_size[0],
                                 self.maze_size[1])
        self.center = center
        for row, maze_row in enumerate(self.maze):
            for col, cell in enumerate(maze_row):
                x = center[0] + col * self.CELL_SIZE
                y = center[1] + row * self.CELL_SIZE
                if cell & 1:
                    self.draw_wall_at((x, y), (x + self.CELL_SIZE, y))
                if cell & 2:
                    self.draw_wall_at((x + self.CELL_SIZE, y),
                                      (x + self.CELL_SIZE,
                                       y + self.CELL_SIZE))
                if cell & 4:
                    self.draw_wall_at(
                        (x, y + self.CELL_SIZE),
                        (x + self.CELL_SIZE, y + self.CELL_SIZE)
                    )
                if cell & 8:
                    self.draw_wall_at(
                        (x, y),
                        (x, y + self.CELL_SIZE)
                    )
        self.maze_surface = self.copy()
        self.player = Player(self.maze, self.lives, self.CELL_SIZE)
        self.pacgums: set[tuple[int, int]] = {
            (row, col)
            for row, maze_row in enumerate(self.maze)
            for col, cell in enumerate(maze_row)
            if cell != 15
        }
        self.pacgums.remove(self.player.get_start(self.maze))
        rows, cols = len(self.maze), len(self.maze[0])
        self.super_pacgums = {
            (0, 0),
            (0, cols - 1),
            (rows - 1, 0),
            (rows - 1, cols - 1)
        }
        for super_pacgum in self.super_pacgums:
            self.pacgums.remove(super_pacgum)

    def start(self, window: pygame.Surface) -> str:
        self.setup()
        clock = pygame.time.Clock()
        run = True
        while run:
            dt = clock.tick(60) / 1000
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    run = False
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        run = False
                    elif e.key == pygame.K_RETURN:
                        return "main"
                    else:
                        self.player.handle_key(e.key)
            pos = (self.player.row, self.player.col)
            if pos in self.pacgums:
                self.pacgums.remove(pos)
                self.player.score += self.points_per_pacgum
            if pos in self.super_pacgums:
                self.super_pacgums.remove(pos)
                self.player.score += self.points_per_super_pacgum
            self.player.update(dt)
            self.blit(self.maze_surface, (0, 0))
            self.draw_pacgums()
            self.draw_score()
            self.player.draw(self, self.center, self.CELL_SIZE)
            window.blit(self, (0, 0))
            pygame.display.update()
        return "exit"
