import pygame
import random

BREDDE, HOYDE = 800, 600
MORK_BLA    = (5, 5, 20)
GRA         = (150, 150, 150)
ROD         = (200, 30, 30)

class Vegg:
    def __init__(self):
        self.w = 15
        self.aktiv = False
        self._reset()

    def _reset(self):
        """Setter veggen til en ny tilfeldig tilstand på høyre side"""
        self.x = BREDDE + 50
        # Tilfeldig høyde
        self.h = random.randint(100, 250)
        # Tilfeldig vertikal posisjon, men ikke for høyt oppe
        self.y = random.randint(50, HOYDE - self.h - 50)
        # Sakket ned farten (før 3-6, nå 1-3)
        self.fart = random.randint(1, 3)
        self.aktiv = True

    def oppdater(self):
        if self.aktiv:
            self.x -= self.fart
            # Hvis den forsvinner ut til venstre
            if self.x + self.w < 0:
                self.aktiv = False
        else:
            # Sjanse for å dukke opp igjen
            if random.random() < 0.01:
                self._reset()

    def tegn(self, skjerm):
        if self.aktiv:
            pygame.draw.rect(skjerm, GRA, (self.x, self.y, self.w, self.h))
            pygame.draw.rect(skjerm, ROD, (self.x, self.y, self.w, self.h), 1)

class Spill:
    def __init__(self):
        pygame.init()
        self.skjerm = pygame.display.set_mode((BREDDE, HOYDE))
        pygame.display.set_caption("Vegg som flyter forbi")
        self.klokke = pygame.time.Clock()
        self.kjorer = True
        
        # Kun veggen er igjen her
        self.vegg = Vegg()

    def kjor(self):
        while self.kjorer:
            # 1. Hendelser
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.kjorer = False

            # 2. Oppdatering
            self.vegg.oppdater()

            # 3. Tegning
            self.skjerm.fill(MORK_BLA)
            self.vegg.tegn(self.skjerm)
            
            pygame.display.flip()
            self.klokke.tick(60)
            
        pygame.quit()

if __name__ == "__main__":
    Spill().kjor()