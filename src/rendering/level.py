from typing import Tuple
import pygame
from mazegenerator import MazeGenerator


class Level(pygame.Surface):
    def __init__(
        self, m_size: Tuple[int, int], *args: int, **kwargs: str
    ) -> None:
        self.CELL_SIZE = 50
        self.maze_size = m_size
        self.maze = MazeGenerator(m_size).maze
        self.WALL_COLOR = (255, 255, 255)
        super().__init__(*args, **kwargs)

    def get_center(self, width: int, height: int) -> Tuple[int, int]:
        s_width, s_height = self.get_size()
        m_width = width * self.CELL_SIZE
        m_height = height * self.CELL_SIZE
        center = ((s_width - m_width) // 2,
                  (s_height - m_height) // 2)
        return center

    def draw_wall_at(self, start: int, end: int) -> None:
        pygame.draw.line(
            self, (255, 255, 255), start, end, 1
        )

    def setup(self) -> None:
        self.fill((0, 0, 0))
        center = self.get_center(self.maze_size[0],
                                 self.maze_size[1])
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

    def start(self, window: pygame.Surface) -> str:
        self.setup()
        run = True
        while run:
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    run = False
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        run = False
                    elif e.key == pygame.K_RETURN:
                        return "main"
            window.blit(self, (0, 0))
            pygame.display.update()
        return "exit"
