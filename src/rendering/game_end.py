from typing import Any
import json
import pygame
from pathlib import Path
from .custom_surface import CustomSurface


class GameEnd(CustomSurface):
    def __init__(self, highscore_path: str, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.highscore_path = Path("./" + highscore_path)

    def setup(self,
              window: pygame.Surface, result: str, score: int) -> None:
        super().setup(window)
        text = "You win!"
        if result == "loser":
            text = "You lost. . ."
        font = pygame.font.Font(self.font_path, 150)
        text_surface = font.render(text, True, pygame.Color("white"))
        w, h = window.get_size()
        t_w, t_h = text_surface.get_size()
        pos_x = (w - t_w) // 2
        pos_y = (h - t_h) // 5
        score_text = f"Score: {score}"
        font = pygame.font.Font(self.font_path, 50)
        score_surface = font.render(score_text, True, pygame.Color("white"))
        user_input = font.render(
            "Add your name: ", True, pygame.Color("White")
        )
        self.blit(text_surface, (pos_x, pos_y))
        self.blit(score_surface, (pos_x + 250, pos_y * 2.1))
        self.blit(user_input, (pos_x + 185, pos_y * 3))

    def valid_name(self, name: str) -> bool:
        return len(name.strip()) >= 2

    def start(self, window: pygame.Surface,
              winner: str, score: int) -> str:
        self.setup(window, winner, score)
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
                            try:
                                with open(self.highscore_path, "r") as f:
                                    scores = json.load(f)
                            except (FileNotFoundError, json.JSONDecodeError):
                                scores = []
                            scores.append({"name": name, "score": score})
                            scores = sorted(scores, key=lambda x: x['score'],
                                            reverse=True)[:10]
                            with open(self.highscore_path, "w") as f:
                                json.dump(scores, f, indent=4)
                            return "main"
                    elif e.key == pygame.K_ESCAPE:
                        return "exit"
                    elif e.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                        self.setup(window, winner, score)
                elif e.type == pygame.TEXTINPUT:
                    name += e.text
                    self.setup(window, winner, score)
            res = font.render(name, True, pygame.Color("white"))
            w, h = window.get_size()
            r_w, r_h = res.get_size()
            x = (w - r_w) // 2
            y = (h - r_h) // 2
            self.blit(res, (x, y * 1.2))
            window.blit(self, (0, 0))
            pygame.display.update()
        return "exit"
