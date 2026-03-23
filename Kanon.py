import pygame, random, math

# --- KONFIGURASJON OG FARGER ---
pygame.init()
BREDDE, HOYDE = 800, 600
skjerm = pygame.display.set_mode((BREDDE, HOYDE))
pygame.display.set_caption("Kanon med mørke boomerang-raketter")
klokke = pygame.time.Clock()

# Fargepalett
MORK_BLA    = (5, 5, 20)
GRA         = (150, 150, 150)
MORK_GRA    = (60, 60, 60)
RAKETT_MORK = (30, 30, 40)  # Ny mørk farge for rakettkroppen
ROD         = (200, 30, 30)
ORANSJE     = (255, 120, 0)
GUL         = (255, 230, 0)

# --- KLASSER ---

class Kanon:
    def __init__(self, x):
        self.x = x
        self.y = HOYDE // 2
        self.fart = 2           
        self.retning = 1        
        self.lop_lengde = 75    

    def oppdater(self):
        # Beveger kanonen opp og ned
        self.y += self.fart * self.retning
        if self.y <= 80 or self.y >= HOYDE - 80:
            self.retning *= -1

    def tegn(self):
        # Tegner kanonløpet
        pygame.draw.rect(skjerm, MORK_GRA, (self.x - 40, self.y - 18, 40, 36))
        pygame.draw.rect(skjerm, GRA, (self.x - 70, self.y - 12, 35, 24))
        pygame.draw.rect(skjerm, (80, 80, 80), (self.x - 75, self.y - 15, 5, 30))

        # Tegner basen
        pygame.draw.circle(skjerm, (80, 80, 80), (self.x, self.y), 35)
        pygame.draw.circle(skjerm, GRA, (self.x, self.y), 30)
        
        # Roterende detaljer på basen
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
        self.farge_indre = RAKETT_MORK # Mørk indre farge

    def oppdater(self):
        # Flytter raketten mot venstre
        self.x -= self.fart
        # Sinus-bølge for en "flyvende" effekt
        self.y += math.sin(pygame.time.get_ticks() * 0.005 + self.offset) * 2

    def tegn(self):
        # 1. FLAMME (Pulserende bak)
        f_str = random.randint(10, 18)
        flamme_start_x = self.x + self.lengde // 2
        
        # Ytre flamme
        pygame.draw.polygon(skjerm, ORANSJE, [
            (flamme_start_x, self.y),
            (flamme_start_x + f_str, self.y - 5),
            (flamme_start_x + f_str + 3, self.y),
            (flamme_start_x + f_str, self.y + 5)
        ])
        # Indre flamme (Gul sirkel)
        pygame.draw.circle(skjerm, GUL, (int(flamme_start_x + 3), int(self.y)), 3)

        # 2. BOOMERANG-PIL FORM (Mørk farge)
        punkter = [
            (self.x, self.y),                                      # Spissen (venstre)
            (self.x + self.lengde // 2, self.y - self.bredde // 2), # Øvre bøy bak
            (self.x + self.lengde, self.y - self.bredde // 4),      # Øvre ende
            (self.x + self.lengde // 2, self.y),                   # Midtpunkt bak
            (self.x + self.lengde, self.y + self.bredde // 4),      # Nedre ende
            (self.x + self.lengde // 2, self.y + self.bredde // 2), # Nedre bøy bak
        ]
        
        # Tegner selve formen med den nye mørke fargen
        pygame.draw.polygon(skjerm, self.farge_indre, punkter)
        # Legger til en rød kantlinje så den ikke forsvinner helt i bakgrunnen
        pygame.draw.polygon(skjerm, ROD, punkter, 2)

        # 3. DETALJ: Liten rød spiss helt foran
        pygame.draw.polygon(skjerm, ROD, [
            (self.x, self.y),
            (self.x + 8, self.y - 3),
            (self.x + 8, self.y + 3)
        ])

# --- HOVEDLØKKE ---

kanon = Kanon(BREDDE - 10)
raketter = []

# Timer for automatisk skyting
SKYT_TIMER = pygame.USEREVENT + 1
pygame.time.set_timer(SKYT_TIMER, 900)

kjorer = True
while kjorer:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            kjorer = False
        
        if event.type == SKYT_TIMER:
            start_x = kanon.x - kanon.lop_lengde
            raketter.append(BoomerangRakett(start_x, kanon.y, random.randint(5, 8)))

    # Oppdatering
    kanon.oppdater()
    for r in raketter[:]:
        r.oppdater()
        if r.x < -100:
            raketter.remove(r)

    # Tegning
    skjerm.fill(MORK_BLA)
    
    for r in raketter:
        r.tegn()
        
    kanon.tegn()

    pygame.display.flip()
    klokke.tick(60)

pygame.quit()