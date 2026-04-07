"""
Dette er staten for hovedmenyen.
"""

from states.base_state import BaseState
import pygame

BREDDE, HOYDE = 800, 600
skjerm = pygame.display.set_mode((BREDDE, HOYDE))

MORK_BLA    = (5, 5, 20)

class MenuState(BaseState):
    def __init__(self):
        super().__init__()

        # Leger et mørkt filter oppå bilde
        self.mork_film = pygame.Surface((800, 600))
        self.mork_film.fill ((0, 0, 0))
        self.mork_film.set_alpha(130) # Jo høyere tall, jo mørkere (0-255)

        try:
            self.bakgrunn_img = pygame.image.load("pix_art.jpg").convert()
            self.bakgrunn = pygame.transform.scale(self.bakgrunn_img, (BREDDE, HOYDE))
        except:
            # Fallback hvis filen mangler
            self.bakgrunn = pygame.Surface((BREDDE, HOYDE))
            self.bakgrunn.fill(MORK_BLA)

    def handle_events(self, events : list[pygame.event.Event]):
        for event in events:
            if event.type == pygame.QUIT:
                self.next_state = None
                self.done = True
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.next_state = "GAME"
                    self.done = True

    def update(self, dt: float):
        pass

    def draw(self, surface: pygame.Surface):
        # 1. Tegn bakgrunnen først
        
        surface.blit(self.bakgrunn, (0, 0))
        surface.blit(self.mork_film, (0, 0))
        self.draw_text(surface, "Du er i hovedmenyen! Trykk SPACE for å starte.", self.font, (255, 255, 255,), (250, 250))
