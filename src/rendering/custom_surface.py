import pygame


class CustomSurface(pygame.Surface):
    def __init__(self,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sprites_dir = "./pacraft_assets"
        self.font_path = "src/config/Minecraft.ttf"

    def setup(self, window: pygame.Surface) -> None:
        self.fill((0, 0, 0))
        self.draw_background(window)

    def draw_background(self, window: pygame.Surface):
        cell = pygame.image.load(f"{self.sprites_dir}/Grass_background.png").convert_alpha()
        w, h = window.get_size()
        c_w, c_h = cell.get_size()
        total_rows = (w // c_w)
        total_cols = h // c_h
        for row in range(total_rows):
            for col in range(total_cols + 1):
                coord = (row * c_w, col * c_h)
                self.blit(cell, coord)