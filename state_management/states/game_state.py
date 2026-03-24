"""
Dette er staten for spillet. Det er her du legger til Spillobjekter, logikk, etc...
"""

from states.base_state import BaseState
import pygame

class GameState(BaseState):
    def __init__(self):
        super().__init__()

    def handle_events(self, events : list[pygame.event.Event]):
        for event in events:
            if event.type == pygame.QUIT:
                self.next_state = None
                self.done = True
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.next_state = "MENU"
                    self.done = True

    def update(self, dt: float):
        pass

    def draw(self, surface: pygame.Surface):
        surface.fill((0, 0, 0))
        self.draw_text(surface, "Du er i spillet! Trykk ESC for å gå tilbake til hovedmenyen.", self.font, (255, 255, 255), (250, 250))

