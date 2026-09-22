import math
from typing import Tuple
import pygame
from mazegenerator import MazeGenerator
from src.config import Config, CHEATS
from src.entities import Player, Ghosts
from .custom_surface import CustomSurface


class Level(CustomSurface):
    def __init__(
        self, configs: Config, size: Tuple[int, int]
    ) -> None:
        super().__init__(size)
        self.CELL_SIZE = 50
        self.forbidden = pygame.image.load(
            f"{self.sprites_dir}/water_block.png")
        self.current_level = 1
        self.CHEAT_BUTTONS = {
            pygame.K_i: "invincible_mode",
            pygame.K_e: "always_edible",
            pygame.K_f: "ghost_freeze",
            pygame.K_l: "skip_level",
            pygame.K_MINUS: "slow_ghost_speed",
            pygame.K_EQUALS: "increase_player_speed",
            pygame.K_g: "add_ghost",
            pygame.K_x: "extra_life"
        }
        self.max_time = 100
        self.timer = self.max_time
        self.paused = False
        self.width = configs.width
        self.height = configs.height
        self.maze_size = (self.width, self.height)
        self.maze = MazeGenerator(size=self.maze_size, seed=configs.seed).maze
        self.WALL_COLOR = (255, 255, 255)
        self.lives = configs.lives
        self.points_per_pacgum = configs.points_per_pacgum
        self.points_per_super_pacgum = configs.points_per_super_pacgum
        self.points_per_ghost = configs.points_per_ghost
        self.font = pygame.font.Font(self.font_path, 40)

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
        x1, y1 = start
        x2, y2 = end
        double = False
        if abs(x2 - x1) > abs(y2 - y1):
            wall = pygame.image.load(
                "pacraft_assets/wall_north_south.png"
            ).convert_alpha()
        else:
            double = True
            wall = pygame.image.load(
                "pacraft_assets/wall_top.png").convert_alpha()
        dx = x2 - x1
        dy = y2 - y1
        ln = int(math.hypot(dx, dy))
        if not ln:
            ln = 1
        wall_thickness = wall.get_height()
        if double:
            wall_thickness *= 2
        scaled = pygame.transform.scale(wall, (ln, wall_thickness))
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        rect = scaled.get_rect(center=(mid_x, mid_y))
        self.blit(scaled, rect.topleft)

    def draw_pacgums(self) -> None:
        gum = pygame.image.load("pacraft_assets/Emerald.png").convert_alpha()
        half = self.CELL_SIZE // 6
        s = gum.get_size()
        scale = 0.7
        new_s = (scale * s[0], scale * s[1])
        gum = pygame.transform.scale(gum, new_s)
        for row, col in self.pacgums:
            x = self.center[0] + col * self.CELL_SIZE + (half * 1.5)
            y = self.center[1] + row * self.CELL_SIZE + (half * 1.5)
            self.blit(gum, (x, y))
        sword = pygame.image.load(
            "pacraft_assets/nether_sword.png").convert_alpha()
        for row, col in self.super_pacgums:
            x = self.center[0] + col * self.CELL_SIZE + half
            y = self.center[1] + row * self.CELL_SIZE + half
            self.blit(sword, (x, y))

    def draw_level_and_timer(self) -> None:
        message = f"Level-{self.current_level} Time: {self.timer}"
        if self.timer <= 10:
            mes_rect = self.font.render(message, True, (252, 3, 3))
        else:
            mes_rect = self.font.render(message, True, (255, 255, 255))
        w = self.get_width()
        size = ((w - mes_rect.get_width()) // 2, 20)
        self.blit(mes_rect, size)

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

    def life_lost(self) -> None:
        self.player.row, self.player.col = self.player.get_start(self.maze)
        for ghost in self.ghosts.ghosts:
            ghost.reset(self.ghosts.speed)
            match ghost.name:
                case "BLINKY":
                    ghost.skin("pacraft_assets/Enderman_front.png")
                case "INKY":
                    ghost.skin("pacraft_assets/Zombie_front.png")
                case "PINKY":
                    ghost.skin("pacraft_assets/Skeletion.png")
                case "CLYDE":
                    ghost.skin("pacraft_assets/Spider_front.png")


    def eat_super_pacgum(self, pos: tuple[int, int]) -> None:
        self.super_pacgums.remove(pos)
        self.player.score += self.points_per_super_pacgum
        for ghost in self.ghosts.ghosts:
            ghost.make_edible()

    def level_passed(self) -> bool:
        return not self.pacgums and not self.super_pacgums

    def check_cheats(self, window: pygame.Surface) -> None:
        if CHEATS["slow_ghost_speed"]:
            self.ghosts.slow_ghosts_speed()
            CHEATS["slow_ghost_speed"] = False
        if CHEATS["extra_life"]:
            self.player.lives += 1
            CHEATS["extra_life"] = False
        if CHEATS["increase_player_speed"]:
            self.player.speed += 0.5
            CHEATS["increase_player_speed"] = False
        if CHEATS["skip_level"]:
            self.advance(window)
            CHEATS["skip_level"] = False
        if CHEATS['add_ghost']:
            self.ghosts.add_ghost()
            CHEATS['add_ghost'] = False

    def setup(self, window: pygame.Surface) -> None:
        self.fill((0, 0, 0))
        self.paused = False
        super().setup(window)
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
                if cell == 15:
                    self.blit(self.forbidden, (x + 10, y + 10))
        self.maze_surface = self.copy()
        self.player = Player(self.maze, self.lives, self.CELL_SIZE)
        self.ghosts = Ghosts(self.maze, self.CELL_SIZE)
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
        self.total_pacgums = len(self.pacgums)

    def advance(self, window: pygame.Surface):
        if self.current_level == 10:
            return "winner:" + str(self.player.score)
        self.current_level += 1
        self.max_time -= 5
        self.timer = self.max_time
        self.maze = MazeGenerator((self.width,
                                  self.height)).maze
        self.setup(window)
        return ""
        

    def start(self, window: pygame.Surface) -> str:
        for c in CHEATS.keys():
            CHEATS[c] = False
        self.timer = self.max_time
        self.setup(window)
        self.player.change_skin("pacraft_assets/Steve_front.png")
        TIMER = pygame.USEREVENT + 1
        pygame.time.set_timer(TIMER, 1000)
        clock = pygame.time.Clock()
        run = True
        while run:
            self.check_cheats(window)
            if not self.timer:
                all_cells = self.width * self.height
                for i in range(all_cells):
                    self.ghosts.add_ghost()
                    self.ghosts.draw(self, self.center)
                    window.blit(self, (0, 0))
                    pygame.display.update()
                return "loser:" + str(self.player.score)
            dt = clock.tick(60) / 1000
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    run = False
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        return "main"
                    elif e.key == pygame.K_RETURN:
                        run = False
                    elif e.key == pygame.K_p:
                        self.paused = not self.paused
                    elif e.key in self.CHEAT_BUTTONS:
                        key = self.CHEAT_BUTTONS[e.key]
                        CHEATS[key] = not CHEATS[key]
                        CHEATS["cheater"] = True
                        match key:
                            case "always_edible":
                                if CHEATS["always_edible"]:
                                    self.ghosts.always_edible()
                                else:
                                    self.ghosts.not_always_edible()
                            case "ghost_freeze":
                                if CHEATS["ghost_freeze"]:
                                    self.ghosts.freeze()
                                else:
                                    self.ghosts.unfreeze()
                    else:
                        self.player.handle_key(e.key)
                elif e.type == TIMER and not self.paused:
                    self.timer -= 1
            if self.paused:
                dt = 0
                continue
            pos = (self.player.row, self.player.col)
            if pos in self.pacgums:
                self.pacgums.remove(pos)
                self.player.score += self.points_per_pacgum
            if pos in self.super_pacgums:
                self.eat_super_pacgum(pos)
            killed, ate = self.ghosts.collide(pos)
            if ate:
                self.player.score += self.points_per_ghost
            if killed:
                self.player.lives -= 1
                if self.player.lives != 0:
                    self.life_lost()
                else:
                    all_cells = self.width * self.height
                    for i in range(all_cells):
                        self.ghosts.add_ghost()
                        self.ghosts.draw(self, self.center)
                        window.blit(self, (0, 0))
                        pygame.display.update()
                    return "loser:" + str(self.player.score)
            if self.level_passed():
                game_end = self.advance(window)
                if game_end:
                    return game_end
            self.player.update(dt)
            self.ghosts.update(
                dt, (self.player.col, self.player.row),
                self.player.facing,
                len(self.pacgums) / self.total_pacgums
            )
            self.blit(self.maze_surface, (0, 0))
            self.draw_pacgums()
            self.draw_level_and_timer()
            self.draw_score()
            self.player.draw(self, self.center, self.CELL_SIZE)
            self.ghosts.draw(self, self.center)
            window.blit(self, (0, 0))
            pygame.display.update()
        return "exit"
