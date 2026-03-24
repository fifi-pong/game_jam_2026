import pygame, random, math
 
BREDDE, HOYDE = 800, 600
MORK_BLA    = (5, 5, 20)
GRA         = (150, 150, 150)
MORK_GRA    = (60, 60, 60)
RAKETT_MORK = (30, 30, 40)
ROD         = (200, 30, 30)
ORANSJE     = (255, 120, 0)
GUL         = (255, 230, 0)

class Kanon:
    def __init__(self, x):
        self.x = x
        self.y = HOYDE // 2
        self.fart = 2           
        self.retning = 1        
        self.lop_lengde = 75    

    def oppdater(self):
        self.y += self.fart * self.retning
        if self.y <= 80 or self.y >= HOYDE - 80:
            self.retning *= -1

    def tegn(self, skjerm):
        # Tegner kanonløpet
        pygame.draw.rect(skjerm, MORK_GRA, (self.x - 40, self.y - 18, 40, 36))
        pygame.draw.rect(skjerm, GRA, (self.x - 70, self.y - 12, 35, 24))
        pygame.draw.rect(skjerm, (80, 80, 80), (self.x - 75, self.y - 15, 5, 30))

        # Tegner basen
        pygame.draw.circle(skjerm, (80, 80, 80), (self.x, self.y), 35)
        pygame.draw.circle(skjerm, GRA, (self.x, self.y), 30)
        
        # Roterende detaljer
        for i in range(4):
            v = (pygame.time.get_ticks() * 0.002) + (i * (math.pi / 2))
            pygame.draw.circle(skjerm, MORK_GRA, (int(self.x + math.cos(v)*20), int(self.y + math.sin(v)*20)), 4)

class BoomerangRakett:
    def __init__(self, x, y, fart):
        self.x, self.y = x, y
        self.fart = fart
        self.lengde = 40  
        self.bredde = 15  
        self.offset = random.random() * 10 
        self.farge_indre = RAKETT_MORK

    def oppdater(self):
        self.x -= self.fart
        self.y += math.sin(pygame.time.get_ticks() * 0.005 + self.offset) * 2

    def tegn(self, skjerm):
        punkter = [
            (self.x, self.y),
            (self.x + self.lengde // 2, self.y - self.bredde // 2),
            (self.x + self.lengde, self.y - self.bredde // 4),
            (self.x + self.lengde // 2, self.y),
            (self.x + self.lengde, self.y + self.bredde // 4),
            (self.x + self.lengde // 2, self.y + self.bredde // 2),
        ]
        pygame.draw.polygon(skjerm, self.farge_indre, punkter)
        pygame.draw.polygon(skjerm, ROD, punkter, 2)

class Spill:
    def __init__(self):
        pygame.init()
        self.skjerm = pygame.display.set_mode((BREDDE, HOYDE))
        pygame.display.set_caption("Kanon m/ OOP")
        self.klokke = pygame.time.Clock()
        self.kjorer = True
        
        # Objekter
        self.kanon = Kanon(BREDDE - 10)
        self.raketter = []
        
        # Timer for skyting
        self.SKYT_TIMER = pygame.USEREVENT + 1
        pygame.time.set_timer(self.SKYT_TIMER, 900)

    def _handter_hendelser(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.kjorer = False
            
            if event.type == self.SKYT_TIMER:
                self._skyt()

    def _skyt(self):
        start_x = self.kanon.x - self.kanon.lop_lengde
        ny_rakett = BoomerangRakett(start_x, self.kanon.y, random.randint(5, 8))
        self.raketter.append(ny_rakett)

    def _oppdater(self):
        self.kanon.oppdater()
        for r in self.raketter[:]:
            r.oppdater()
            if r.x < -100:
                self.raketter.remove(r)

    def _tegn(self):
        self.skjerm.fill(MORK_BLA)
        
        for r in self.raketter:
            r.tegn(self.skjerm)
            
        self.kanon.tegn(self.skjerm)
        pygame.display.flip()

    def kjor(self):
        """Hovedløkken til spillet"""
        while self.kjorer:
            self._handter_hendelser()
            self._oppdater()
            self._tegn()
            self.klokke.tick(60)
        pygame.quit()

if __name__ == "__main__":
    spill = Spill()
    spill.kjor()