from typing import Tuple
import pygame


class Button:
    def __init__(
        self, name: str, x: int,
        y: int, size: Tuple[int, int],
        text: str, font: str, font_s: int
    ) -> None:
        self.name = name
        self.text = text
        self.rect = pygame.Rect(x,
                                y,
                                size[0],
                                size[1])
        self.font = pygame.font.SysFont(font, font_s)
        self.clicked = False

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(
            surface,
            pygame.Color("grey"),
            self.rect,
            width=3
        )
        text_surf = self.font.render(self.text, True,
                                     pygame.Color("white"))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_click(self) -> bool:
        return self.rect.collidepoint(pygame.mouse.get_pos())
