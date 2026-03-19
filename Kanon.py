import pygame, random, math

# --- KONFIGURASJON OG FARGER ---
pygame.init()
BREDDE, HOYDE = 800, 600
skjerm = pygame.display.set_mode((BREDDE, HOYDE))
pygame.display.set_caption("Kanon med detaljerte raketter")
klokke = pygame.time.Clock()

# Fargepalett
MORK_BLA    = (5, 5, 20)
GRA         = (150, 150, 150)
MORK_GRA    = (60, 60, 60)
ROD         = (200, 30, 30)
ORANSJE     = (255, 120, 0)
GUL         = (255, 230, 0)
LYS_BLA     = (170, 220, 255) # For vinduet på raketten

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

class Rakett:
    def __init__(self, x, y, fart):
        self.x, self.y = x, y
        self.fart = fart
        self.bredde = 35
        self.hoyde = 16
        self.offset = random.random() * 10 
        self.farge_kropp = (130, 130, 140)

    def oppdater(self):
        self.x -= self.fart
        # Sinus-bølge for en "flyvende" effekt
        self.y += math.sin(pygame.time.get_ticks() * 0.005 + self.offset) * 2

    def tegn(self):
        # 1. FLAMME (Pulserende bak)
        f_str = random.randint(15, 25)
        # Ytre flamme (Oransje)
        pygame.draw.polygon(skjerm, ORANSJE, [
            (self.x + self.bredde, self.y),
            (self.x + self.bredde + f_str, self.y - 7),
            (self.x + self.bredde + f_str + 5, self.y),
            (self.x + self.bredde + f_str, self.y + 7)
        ])
        # Indre flamme (Gul)
        pygame.draw.circle(skjerm, GUL, (int(self.x + self.bredde + 4), int(self.y)), 5)

        # 2. KROPP (Hoveddel)
        pygame.draw.rect(skjerm, self.farge_kropp, (self.x, self.y - self.hoyde//2, self.bredde, self.hoyde))
        # Detalj: En mørk stripe på midten for tekstur
        pygame.draw.rect(skjerm, MORK_GRA, (self.x + 10, self.y - self.hoyde//2, 5, self.hoyde))

        # 3. SPISS (Trekant foran)
        pygame.draw.polygon(skjerm, ROD, [
            (self.x, self.y - self.hoyde//2),
            (self.x - 15, self.y),
            (self.x, self.y + self.hoyde//2)
        ])

        # 4. VINDU (Liten cockpit)
        pygame.draw.circle(skjerm, LYS_BLA, (int(self.x + 5), int(self.y)), 4)

        # 5. FINNER (Vinger bak)
        # Øvre finne
        pygame.draw.polygon(skjerm, ROD, [
            (self.x + self.bredde - 10, self.y - self.hoyde//2),
            (self.x + self.bredde + 5, self.y - self.hoyde//2 - 8),
            (self.x + self.bredde, self.y - self.hoyde//2)
        ])
        # Nedre finne
        pygame.draw.polygon(skjerm, ROD, [
            (self.x + self.bredde - 10, self.y + self.hoyde//2),
            (self.x + self.bredde + 5, self.y + self.hoyde//2 + 8),
            (self.x + self.bredde, self.y + self.hoyde//2)
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
            raketter.append(Rakett(start_x, kanon.y, random.randint(5, 8)))

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