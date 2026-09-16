import pygame


class CustomSurface(pygame.Surface):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keys = {
            pygame.K_ESCAPE: ""
        }

    def check_event(self):
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                return False

    def check_key_press(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            return pygame.K_ESCAPE
        elif keys[pygame.K_RETURN]:
            return pygame.K_RETURN
