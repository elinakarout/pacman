from typing import Any
import json
import pygame
from pathlib import Path
from src.config import CHEATS
from .custom_surface import CustomSurface


class GameEnd(CustomSurface):
    def __init__(self, highscore_path: str, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.highscore_path = Path("./" + highscore_path)

    def wrap_text(
        self, text: str, font: pygame.font.Font, max_width: int
    ) -> list[str]:
        words = text.split()
        lines = []
        current = ""
        for word in words:
            candidate = f"{current} {word}".strip()
            if font.size(candidate)[0] <= max_width or not current:
                current = candidate
            else:
                lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines

    def setup(self,
              window: pygame.Surface, result: str, score: int) -> None:
        super().setup(window)
        cheater = CHEATS["cheater"]
        font_size = 150
        if not cheater:
            text = "You win!"
            if result == "loser":
                text = "You lost. . ."
        else:
            font_size = 70
            text = ("Of course you will win you loser. "
                    "You couldn't win this game without cheating")
            if result == "loser":
                text = ("Even while cheating you couldn't win this game. "
                        "You are a failure.")
            score = -42
        w, h = window.get_size()
        font = pygame.font.Font(self.font_path, font_size)
        lines = self.wrap_text(text, font, w - 100)
        line_surfaces = [
            font.render(line, True, pygame.Color("white")) for line in lines
        ]
        line_height = font.get_linesize()
        block_height = line_height * len(line_surfaces)
        pos_y = (h - block_height) // 5
        for i, line_surface in enumerate(line_surfaces):
            t_w = line_surface.get_width()
            pos_x = (w - t_w) // 2
            self.blit(line_surface, (pos_x, pos_y + i * line_height))
        block_bottom = pos_y + block_height
        score_text = f"Score: {score}"
        font = pygame.font.Font(self.font_path, 50)
        score_surface = font.render(score_text, True, pygame.Color("white"))
        user_input = font.render(
            "Add your name: ", True, pygame.Color("White")
        )
        score_x = (w - score_surface.get_width()) // 2
        input_x = (w - user_input.get_width()) // 2
        input_y = block_bottom + 120
        self.blit(score_surface, (score_x, block_bottom + 60))
        self.blit(user_input, (input_x, input_y))
        self.name_input_y = input_y + user_input.get_height() + 20

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
            self.blit(res, (x, self.name_input_y))
            window.blit(self, (0, 0))
            pygame.display.update()
        return "exit"
