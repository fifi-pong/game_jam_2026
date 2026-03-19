import pygame, random, math

# --- OPPSETT OG FARGER ---
pygame.init()
BREDDE, HOYDE = 800, 600
skjerm = pygame.display.set_mode((BREDDE, HOYDE))
klokke = pygame.time.Clock()

MORK_BLA    = (5, 5, 20)
GRA         = (150, 150, 150)
MORK_GRA    = (60, 60, 60)
ROD         = (255, 30, 30)

# --- KLASSER ---

class Kanon:
    def __init__(self, x):
        self.x = x
        self.y = HOYDE // 2
        self.fart = 2  # Hvor fort kanonen flytter seg opp/ned
        self.retning = 1 # 1 er ned, -1 er opp
        self.lengde = 50
        self.bredde = 35

    def oppdater(self):
        # Flytter kanonen opp eller ned
        self.y += self.fart * self.retning
        
        # Snu retning hvis den treffer topp eller bunn
        if self.y <= 50 or self.y >= HOYDE - 50:
            self.retning *= -1

    def tegn(self):
        # Tegner kanonløpet pekende mot venstre (180 grader / math.pi)
        # Vi tegner den litt "innover" på skjermen fra høyre side
        pygame.draw.rect(skjerm, GRA, (self.x - self.lengde, self.y - self.bredde//2, self.lengde, self.bredde))
        # Tegner basen til kanonen
        pygame.draw.circle(skjerm, MORK_GRA, (self.x, self.y), 30)

class Kanon_Kule:
    def __init__(self, x, y, fart):
        self.x, self.y = x, y
        self.radius = 15
        self.fart = fart
        self.offset = random.random() * 10
        # Re-introduserer kollisjonsboks fra din originale kode
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius*2, self.radius*2)

    def oppdater(self):
        # Flytter kulen mot venstre (slik din originale kode gjorde)
        self.x -= self.fart
        # Den bølgende sinus-bevegelsen fra originalkoden din
        self.y += math.sin(pygame.time.get_ticks() * 0.005 + self.offset) * 2
        self.rect.center = (self.x, self.y)

    def tegn(self):
        # Dine originale roterende pigger
        for i in range(8):
            v = i * (math.pi/4) + (pygame.time.get_ticks() * 0.01)
            pygame.draw.line(skjerm, ROD, (self.x, self.y), (self.x + math.cos(v)*22, self.y + math.sin(v)*22), 2)
        
        # Din originale blinke-effekt
        farge = ROD if (pygame.time.get_ticks() // 200) % 2 == 0 else (50, 0, 0)
        pygame.draw.circle(skjerm, farge, (int(self.x), int(self.y)), self.radius)

# --- HOVEDLØKKE ---

# Plasserer kanonen helt til høyre (BREDDE)
kanon = Kanon(BREDDE - 10)
kuler = []

# Timer for å skyte automatisk
SKYT_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SKYT_EVENT, 800) # Skyter hvert 800. millisekund

kjorer = True
while kjorer:
    skjerm.fill(MORK_BLA)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            kjorer = False
        
        # Skyter automatisk når timeren går av
        if event.type == SKYT_EVENT:
            # Lager en kule som starter ved kanonens munning
            ny_kule = Kanon_Kule(kanon.x - 50, kanon.y, random.randint(4, 8))
            kuler.append(ny_kule)

    # Oppdatering
    kanon.oppdater()
    for kule in kuler[:]:
        kule.oppdater()
        # Fjerner kuler når de forsvinner ut til venstre
        if kule.x < -50:
            kuler.remove(kule)

    # Tegning
    kanon.tegn()
    for kule in kuler:
        kule.tegn()

    pygame.display.flip()
    klokke.tick(60)

pygame.quit()