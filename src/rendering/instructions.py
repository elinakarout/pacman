import pygame

from .custom_surface import CustomSurface


class Instructions(CustomSurface):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.instructions = [
            "Use UP, DOWN, LEFT, RIGHT to move",
            "Collect pacgums to increase score",
            "Press ctrl + D to enable cheats",
            "Evade ghosts",
            "Have fun!"
        ]

    def setup(self, window: pygame.Surface) -> None:
        self.fill((0, 0, 0))
        self.draw_background(window)
        ins_size = (100, 100)
        w, h = self.get_size()
        for i, ins in enumerate(self.instructions):
            ins_x = (w - ins_size[0]) // 2.5
            ins_y = (h - ins_size[1]) // 5 * (i+2) * 0.50
            font = pygame.font.Font(self.font_path, 32)
            font_s = font.render(f"{i+1}. {ins}", True,
                                 pygame.Color("white"))
            self.blit(font_s, (ins_x, ins_y))

    def start(self, window: pygame.Surface):
        self.setup(window)
        run = True
        while run:
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    return False
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RETURN:
                        return "main"
                    elif e.key == pygame.K_ESCAPE:
                        run = False
            window.blit(self, (0, 0))
            pygame.display.update()
        return "exit"