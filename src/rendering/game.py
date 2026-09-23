import pygame
from typing import Dict
from .game_end import GameEnd
from .instructions import Instructions
from .main_menu import MainMenu
from .level import Level
from .highscore import Highscore
from src.config import Config


SURFACE = MainMenu | Level | Highscore | Instructions | GameEnd
SURFACES = Dict[str, SURFACE]


class Game:
    """Game main class."""

    def __init__(self, configs: Config) -> None:
        """Initialize class."""

        self.surfaces: SURFACES = {}
        self.configs = configs
        self.score = 0

    def add_surface(self, name: str, surface: SURFACE) -> None:
        """Add surface."""

        self.surfaces[name] = surface

    def play_scene(self, window: pygame.Surface, scene: str) -> str:
        """Play current scene."""

        answer = scene.split(":")
        if answer[0] == "exit":
            return scene
        elif answer[0] in {"winner", "loser"}:
            game_end = self.surfaces["game_end"]
            assert isinstance(game_end, GameEnd)
            return game_end.start(window, answer[0], int(answer[1]))
        else:
            surface = self.surfaces[scene]
            assert isinstance(
                surface, (MainMenu, Level, Highscore, Instructions)
            )
            return surface.start(window)

    def start(self) -> None:
        """Start screen."""

        pygame.init()
        window = pygame.display.set_mode(flags=pygame.FULLSCREEN)
        pygame.display.set_caption("Pac-Man")
        pygame.display.set_icon(
            pygame.image.load("pacraft_assets/Steve_front.png"))
        self.add_surface("main", MainMenu(window.get_size()))
        self.add_surface("start", Level(self.configs, window.get_size()))
        self.add_surface("highscore", Highscore(
            self.configs.highscore_filename,
            window.get_size())
        )
        self.add_surface("instructions", Instructions(window.get_size()))
        self.add_surface(
            "game_end",
            GameEnd(self.configs.highscore_filename, window.get_size())
        )
        current = "main"
        run = True
        while run:
            if current == "exit":
                run = False
            current = self.play_scene(window, current)
        pygame.quit()
