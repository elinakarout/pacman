from typing import Any, Dict, List, Tuple
import pygame
import json
import os
from .custom_surface import CustomSurface


class Highscore(CustomSurface):
    def __init__(self, file_path: str, size: Tuple[int, int]) -> None:
        self.scores: List[Dict[str, Any]] = []
        self.path = file_path
        super().__init__(size)

    def print_empty(self) -> None:
        font = pygame.font.Font(self.font_path, 32)
        font_s = font.render("No highscores :(", True, pygame.Color("white"))
        w, h = self.get_size()
        f_w, f_h = font_s.get_size()
        title_w = (w - f_w) // 2
        title_h = (h - f_h) // 5
        self.blit(font_s, (title_w, title_h))

    def setup(self, window: pygame.Surface) -> None:
        super().setup(window)
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                self.scores = json.load(f)
            self.scores = sorted(self.scores,
                                 key=lambda x: x['score'],
                                 reverse=True)
        if not self.scores:
            self.print_empty()
            return
        font = pygame.font.Font(self.font_path, 32)
        for i, score in enumerate(self.scores):
            font_s = font.render(f"{i+1}. {score['name']}-{score['score']}",
                                 True, pygame.Color("White"))
            w, h = self.get_size()
            f_w, f_h = font_s.get_size()
            score_w = ((w - f_w) // 2)
            score_h = ((h - f_h) // 6) * (i+1) * 0.25
            self.blit(font_s, (score_w, score_h))

    def start(self, window: pygame.Surface) -> str:
        self.setup(window)
        run = True
        while run:
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    run = False
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        return "main"
                    elif e.key == pygame.K_RETURN:
                        run = False
            w, h = window.get_size()
            f_w, f_h = self.get_size()
            scene_w = ((w - f_w) // 2)
            scene_h = ((h - f_h) // 2)
            window.blit(self, (scene_w, scene_h))
            pygame.display.update()
        return "exit"
