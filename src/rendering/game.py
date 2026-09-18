from typing import Dict
import pygame
from .main_menu import MainMenu
from .level import Level
from .highscore import Highscore
from src.config import Config

SURFACES = Dict[str, pygame.Surface]


class Game:
    def __init__(self, configs:  Config):
        self.surfaces: SURFACES = {}
        self.configs = configs

    def add_surface(self, name: str, surface: pygame.Surface):
        self.surfaces[name] = surface

    def play_scene(self, window: pygame.Surface, scene: str) -> str:
        if scene == "exit":
            return "exit"
        return self.surfaces[scene].start(window)

    def start(self):
        pygame.init()
        window = pygame.display.set_mode(flags=pygame.FULLSCREEN)
        pygame.display.set_caption("Pac-Man")
        self.add_surface("main", MainMenu(window.get_size()))
        self.add_surface("start", Level(self.configs, window.get_size()))
        self.add_surface("highscore", Highscore("src/Rendering/highscore.json", window.get_size()))
        # self.add_surface("instructions", Instructions(window.get_size()))
        current = "main"
        run = True
        while run:
            if current == "exit":
                run = False
            print(f"Currently on: {current}")
            current = self.play_scene(window, current)
        pygame.quit()
