import pygame
from typing import Dict
from .instructions import Instructions
from .main_menu import MainMenu
from .level import Level
from .highscore import Highscore
from src.config import Config

SURFACES = Dict[str, MainMenu | Level | Highscore]


class Game:
    def __init__(self, configs: Config) -> None:
        self.surfaces: SURFACES = {}
        self.configs = configs

    def add_surface(
        self, name: str, surface: MainMenu | Level | Highscore
    ) -> None:
        self.surfaces[name] = surface

    def play_scene(self, window: pygame.Surface, scene: str) -> str:
        if scene == "exit":
            return "exit"
        return self.surfaces[scene].start(window)

    def start(self) -> None:
        pygame.init()
        window = pygame.display.set_mode(flags=pygame.FULLSCREEN)
        pygame.display.set_caption("Pac-Man")
        self.add_surface("main", MainMenu(window.get_size()))
        self.add_surface("start", Level(self.configs, window.get_size()))
        self.add_surface("highscore", Highscore(
            "src/Rendering/highscore.json",
            window.get_size())
        )
        self.add_surface("instructions", Instructions(window.get_size()))
        current = "main"
        run = True
        while run:
            if current == "exit":
                run = False
            current = self.play_scene(window, current)
        pygame.quit()
