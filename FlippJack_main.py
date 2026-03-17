import pygame, random

# 1. Oppsett
class FlippJack:
    pygame.init()
    skjerm = pygame.display.set_mode((800, 600))
    kjorer = True

# 2. Spill-løkken (Game Loop)
while kjorer:
    for hendelse in pygame.event.get():
        if hendelse.type == pygame.QUIT:
            kjorer = False
            
    skjerm.fill((0, 0, 0)) # Gjør skjermen svart
    pygame.display.flip()  # Oppdater skjermen

pygame.quit()