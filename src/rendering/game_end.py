import json
from typing import Tuple
import pygame
from .custom_surface import CustomSurface


class GameEnd(CustomSurface):
    def __init__(self, highscore_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.highscore_path = highscore_path

    def setup(self, window: pygame.Surface,
              res: bool):
        super().setup(window)
        text = "You win!"
        if res == "loser":
            text = "You lost. . ."
        print(text)
        font = pygame.font.Font(self.font_path, 150)
        res = font.render(text, True, pygame.Color("white"))
        w, h = window.get_size()
        t_w, t_h = res.get_size()
        pos_x = (w - t_w) // 2
        pos_y = (h - t_h) // 5
        font = pygame.font.Font(self.font_path, 50)
        user_input = font.render("Add your name: ", True, pygame.Color("White"))
        self.blit(res, (pos_x, pos_y))
        self.blit(user_input, (pos_x + 150, pos_y * 2))

    def valid_name(self, name: str):
        return len(name.strip()) >= 3

    def start(self, window: pygame.Surface,
              winner: bool):
        self.setup(window, winner)
        run = True
        name = ""
        font = pygame.font.Font(self.font_path, 32)
        while run:
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    return "exit"
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RETURN:
                        if self.valid_name(name):
                            with open(self.highscore_path, "r+") as f:
                                scores = json.load(f)
                                lowest = min(scores, key=lambda x: x['score'])
                                # if lowest 
                                scores = sorted(scores, key=lambda x: x['score'],
                                                reverse=True)    
                                if len(scores) >= 10:
                                    scores.popitem()
                                    json.dump(scores, f)
                            return "main"
                    elif e.key == pygame.K_ESCAPE:
                        return "exit"
                    elif e.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                        self.setup(window, winner)
                elif e.type == pygame.TEXTINPUT:
                    name += e.text
                    self.setup(window, winner)
            res = font.render(name, True, pygame.Color("white"))
            w, h = window.get_size()
            r_w, r_h = res.get_size()
            x = (w - r_w) // 2
            y = (h - r_h) // 2
            self.blit(res, (x, y))
            window.blit(self, (0, 0))
            pygame.display.update()
