import pygame, random

# 1. Oppsett
class FlippJack:
    def __init__(self):
        pygame.init()
        self.skjerm = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.running = True

class Objecter:
    def __init__(self):
        pass

class Spiller(Objecter):
    def __init__(self):
        super().__init__()
        pass

class Laser(Objecter):
    def __init__(self):
        super().__init__()
        pass

class Kanon(Objecter):
    def __init__(self):
        super().__init__()
        pass

class Vegger(Objecter):
    def __init__(self):
        super().__init__()
        pass



"""
# 2. Spill-løkken (Game Loop)
while kjorer:
    for hendelse in pygame.event.get():
        if hendelse.type == pygame.QUIT:
            kjorer = False
            
    skjerm.fill((0, 0, 0)) # Gjør skjermen svart
    pygame.display.flip()  # Oppdater skjermen

pygame.quit()
"""