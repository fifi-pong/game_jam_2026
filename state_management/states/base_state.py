"""
En abstrakt klasse for states.

Har lagt til tegnefunksjonalitet som alle States har tilgang til. Her kan du legge til generell funksjonalitet for alle states.
"""

import pygame # For å få autocomplete og typer.
from abc import ABC, abstractmethod # For å lage en abstrakt klasse. Alle states må arve fra denne klassen.

class BaseState(ABC):
    """En abstrakt klasse for states. Alle states må arve fra denne klassen.
    
    Attributter:
        next_state (str): String-navnet til neste state i states-ordboken.
        done (bool): Om staten er ferdig og skal byttes ut. 
    """

    def __init__(self):
        """Initialiserer staten."""
        self.done = False
        self.next_state = None
        self.font = pygame.font.SysFont(None, 20)
        font_stor = pygame.font.SysFont("Arial", 26, bold=True)
        font_liten = pygame.font.SysFont("Arial", 16, bold=True)

    def draw_text(self, surface : pygame.Surface, string : str, font : pygame.font.Font, color : tuple, center : tuple):
        # Lager tekst. Andre parameter er anti-alias. Sett til True for glatt og fin tekst.
        text = font.render(string, False, color)
        # Henter rektangelet rundt teksten, med sentrum der man ønsker.
        text_rect = text.get_rect(center = center)
        # Setter teksten på overflaten man spesifiserte.
        surface.blit(text, text_rect)

    @abstractmethod
    def handle_events(self, events : list[pygame.event.Event]):
        """Håndterer events. Må implementeres av subklasser.
        
        Args:
            events (list[pygame.event.Event]): En liste over pygame-events."""
        pass

    @abstractmethod
    def update(self, dt: float):
        """Oppdaterer staten. Må implementeres av subklasser.
        
        Args:
            dt (float): Tiden som har gått siden forrige oppdatering, i sekunder."""
        pass

    @abstractmethod    
    def draw(self, surface: pygame.Surface):
        """Tegner staten. Må implementeres av subklasser.
        
        Args:
            surface (pygame.Surface): Overflaten som skal tegnes på."""
        pass