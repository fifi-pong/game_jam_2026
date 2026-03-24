"""
En generell spill-klasse. Dette er hovedprogrammet.
"""

import pygame
from states.base_state import BaseState
from states.menu_state import MenuState
from states.game_state import GameState

class Spill:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((500, 500))
        self.clock = pygame.time.Clock()
        self.running = True
        self.states = {
            "MENU": MenuState(),
            "GAME": GameState()
        }
        self.current_state = self.states["MENU"]

    def main_loop(self):
        self.handle_events()
        self.update()
        self.render()

    def handle_events(self):
        events = pygame.event.get()

        # Events håndteres i staten.
        self.current_state.handle_events(events)

    def update(self):
        # Tiden siden forrige oppdatering. Nyttig for å gjøre frame-rate independent bevegelse.
        dt = self.clock.tick(60) / 1000.0

        # Oppdaterer staten.
        self.current_state.update(dt)

        # Sjekker om staten er ferdig. Hvis den er det, bytter vi til neste state.
        if self.current_state.done:
            next_state = self.current_state.next_state
            self.current_state.done = False
            if next_state:
                self.current_state = self.states[next_state]
            else:
                self.running = False

    def render(self):
        # Tegner state
        self.current_state.draw(self.screen)
        pygame.display.flip()

spill = Spill()
while spill.running:
    spill.main_loop()