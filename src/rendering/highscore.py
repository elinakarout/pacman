import pygame
import json
import os


class Highscore(pygame.Surface):
    def __init__(self, file_path: str, *args, **kwargs) -> None:
        self.scores = {}
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                self.scores = json.load(f)
        super().__init__(*args, **kwargs)

    def print_empty(self):
        font = pygame.font.SysFont("arial", 32)
        font_s = font.render("No highscores :(", True, pygame.Color("white"))
        w, h= self.get_size()
        f_w, f_h = font_s.get_size()
        title_w = (w - f_w) // 2
        title_h = (h - f_h) // 5
        self.blit(font_s, (title_w, title_h))

    def setup(self) -> None:
        self.fill((0, 0, 0))
        self.print_empty()

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
            window.blit(self, (0,0))
            pygame.display.update()
        return "exit"
