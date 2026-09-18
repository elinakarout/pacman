from typing import Dict, List
import pygame
from .button import Button

BUTTTONS = Dict[str, Button] | None


class MainMenu(pygame.Surface):
    def __init__(self, *args: int, **kwargs: str) -> None:
        self.buttons: BUTTTONS = {}
        self.states = [
            "start",
            "highscore",
            "instructions",
            "exit"
        ]
        super().__init__(*args, **kwargs)

    def buttons_init(self, width: int, height: int) -> List[Button]:
        OFFSET = 100
        FONT = ("arial", 50)
        BUTTON_SIZE = (300, 100)
        button_x = (width - BUTTON_SIZE[0]) // 2
        button_y = (height - BUTTON_SIZE[1]) // 2
        res = []
        for i, n in enumerate(self.states):
            btn = Button(
                name=n,
                x=button_x,
                y=button_y + (OFFSET * (i * 1.25)),
                size=BUTTON_SIZE,
                text=n.capitalize(),
                font=FONT[0],
                font_s=FONT[1]
            )
            res.append(btn)
        return res

    def setup(self):
        self.fill((0, 0, 0))
        font = pygame.font.SysFont("arial", 150)
        font_s = font.render("Pac-Man", True,
                             pygame.Color("yellow"))
        w, h = self.get_size()
        f_w, f_h = font_s.get_size()
        title_w = (w - f_w) // 2
        title_h = (h - f_h) // 5
        buttons = self.buttons_init(w, h)
        for b in buttons:
            b.draw(self)
            self.buttons[b.name] = b
        self.blit(font_s, (title_w, title_h))

    def check_button_clicked(self):
        buttons = [b for b in self.buttons.values() if b.check_click()]
        return buttons[0] if buttons else None

    def start(self, window: pygame.Surface) -> str:
        self.setup()
        run = True
        for b in self.buttons.values():
            b.draw(self)
        while run:
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    return False
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RETURN:
                        return "start"
                    elif e.key == pygame.K_ESCAPE:
                        run = False
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    button = self.check_button_clicked()
                    if button is not None:
                        return button.name
            window.blit(self, (0, 0))
            pygame.display.update()
        return "exit"
