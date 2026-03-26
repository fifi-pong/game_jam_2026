"""
Dette er staten for hovedmenyen.
"""

from states.base_state import BaseState
import pygame

class MenuState(BaseState):
    def __init__(self):
        super().__init__()
        

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
        surface.fill((255, 0, 0))
        self.draw_text(surface, "Du er i hovedmenyen! Trykk SPACE for å starte.", self.font, (255, 255, 255), (250, 250))
