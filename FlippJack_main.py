import pygame, random, math, sys

# --- KONFIGURASJON ---
pygame.init()
BREDDE, HOYDE = 800, 600
skjerm = pygame.display.set_mode((BREDDE, HOYDE))
pygame.display.set_caption("FlippJack")
clock = pygame.time.Clock()

# --- FARGER ---
MORK_BLA    = (5, 5, 20)
BLACK       = (0, 0, 0)
HVIT        = (255, 255, 255)
GRA         = (150, 150, 150)
MORK_GRA    = (60, 60, 60)
CYAN        = (0, 255, 255)
GUL         = (255, 255, 0)
ORANSJE     = (255, 100, 0)
ROD         = (255, 30, 30)
LYSE_ROD    = (247, 64, 64)
NEON_LILLA  = (180, 0, 255)
PLASM_BLA   = (0, 150, 255)

font_stor = pygame.font.SysFont("Arial", 26, bold=True)
font_liten = pygame.font.SysFont("Arial", 16, bold=True)


# 1. Oppsett
class FlippJack:
    def __init__(self):
        pygame.init() 
        self.keys = pygame.key.get_pressed()
        self.running = True

        self.spiller = Romskip(70, 300)
        self.kanon = Kanon(BREDDE - 10)
        self.kuler = []
        self.skyt_timer = 0  # teller opp tid i millisekunder

        self.laser = Laser(BREDDE // 2)

        self.vegg = Vegg()

        self.poeng = 0

    def main_loop(self):
        self.handel_event()
        self.update()
        self.render()

    def handel_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        self.keys = pygame.key.get_pressed()

    def update(self):
        dt = clock.tick(60) / 1000
        #spilleren
        opp = self.keys[pygame.K_UP]
        ned = self.keys[pygame.K_DOWN]
        venstre = self.keys[pygame.K_LEFT]
        hoyre = self.keys[pygame.K_RIGHT]
        self.spiller.update(opp, ned, venstre, hoyre)

        #kanonen
        self.kanon.update()
        for kule in self.kuler[:]:
            kule.update()
            if kule.x < -50:
                self.kuler.remove(kule)
        
        # Automatisk skyting
        self.skyt_timer += clock.get_time()
        if self.skyt_timer >= 800:
            ny_kule = Kanon_Kule(self.kanon.x - 50, self.kanon.y, random.randint(4, 8))
            self.kuler.append(ny_kule)
            self.skyt_timer = 0

        self.laser.update()

        self.vegg.update()
        self.poeng += dt
    
    def render(self):
        skjerm.fill(MORK_BLA)
        self.spiller.tegn(False)
        self.vegg.tegn(skjerm)
        self.kanon.tegn()
        for kule in self.kuler:
            kule.tegn()
        self.laser.tegn()

        score_text = font_stor.render(f"{round(self.poeng)}", True, HVIT)
        skjerm.blit(score_text, (350, 20))
        pygame.display.flip()


    
#gjennerel oppsett
class Objecter:
    def __init__(self, x, y, bredde, hoyde):
        self.x = x
        self.y = y
        self.bredde = bredde
        self.hoyde = hoyde
        self.color = (100, 100, 100)
        self.rect = pygame.Rect(x - bredde // 2, y - hoyde // 2, bredde, hoyde)

    def update(self):
        pass

    def render(self):
        pass



class Romskip(Objecter):
    def __init__(self, x, y):
        super().__init__(x, y, 45, 22)
        self.fart_y = 0
        self.rect = pygame.Rect(self.x, self.y, self.bredde, self.hoyde)
        self.klapp = 0 
        self.partikler = []

    def update(self, opp, ned, venstre, hoyre):
        acc = 0.5
        friksjon = 0.95
        max_fart = 5

        # lag fart hvis ikke finnes
        if not hasattr(self, "fart_x"):
            self.fart_x = 0

        # GRAVITY
        self.fart_y += 0.2

        # thrust (som motorer)
        if opp:
            self.fart_y -= acc
        if ned:
            self.fart_y += acc
        if venstre:
            self.fart_x -= acc
        if hoyre:
            self.fart_x += acc

        # friksjon
        self.fart_x *= friksjon
        self.fart_y *= friksjon

        # maks fart
        self.fart_x = max(-max_fart, min(self.fart_x, max_fart))
        self.fart_y = max(-max_fart, min(self.fart_y, max_fart))

        # flytt skipet
        self.x += self.fart_x
        self.y += self.fart_y

        # hold deg på skjermen
        self.x = max(0, min(self.x, BREDDE - self.bredde))
        self.y = max(0, min(self.y, HOYDE - self.hoyde))

        self.rect.topleft = (self.x, self.y)

    def tegn(self, skjold_aktiv):
        for p in self.partikler: p.tegn()
        
        # Skjold-effekt
        if skjold_aktiv:
            pygame.draw.circle(skjerm, (0, 255, 150), (int(self.x + 22), int(self.y + 11)), 35, 2)

        # Plasma-flamme
        if self.fart_y < 3:
            f_size = random.randint(20, 35) if self.fart_y < 0 else random.randint(10, 20)
            pygame.draw.polygon(skjerm, PLASM_BLA, [(self.x+2, self.y+6), (self.x-f_size, self.y+11), (self.x+2, self.y+16)])
            pygame.draw.polygon(skjerm, HVIT, [(self.x+2, self.y+9), (self.x-f_size//2, self.y+11), (self.x+2, self.y+13)])

        # Vinger
        bak_x = self.x - 12
        for v_dir in [-1, 1]:
            v_offset = (self.y + 11) + (v_dir * 4)
            klapp_v = v_dir * self.klapp
            p_liste = [(self.x+20, v_offset), (bak_x, v_offset + (v_dir*18) + klapp_v), (self.x+5, v_offset)]
            pygame.draw.polygon(skjerm, MORK_GRA, p_liste)
            pygame.draw.polygon(skjerm, GRA, p_liste, 1)

        # Skrog
        kropp = [(self.x, self.y+6), (self.x+35, self.y+3), (self.x+46, self.y+11), (self.x+35, self.y+19), (self.x, self.y+16)]
        pygame.draw.polygon(skjerm, (80, 80, 90), kropp)
        pygame.draw.polygon(skjerm, (40, 40, 50), kropp, 2)
        
        # Cockpit
        vindu = [(self.x+22, self.y+7), (self.x+34, self.y+7), (self.x+40, self.y+11), (self.x+34, self.y+15), (self.x+22, self.y+15)]
        pygame.draw.polygon(skjerm, (0, 60, 100), vindu)
        pygame.draw.polygon(skjerm, CYAN, vindu, 1)
        

class Kanon: 
    def __init__(self, x):
        self.x = x
        self.y = HOYDE // 2
        self.fart = 2  # Hvor fort kanonen flytter seg opp/ned
        self.retning = 1 # 1 er ned, -1 er opp
        self.lengde = 50
        self.bredde = 35

    def update(self):
        # Flytter kanonen opp eller ned
        self.y += self.fart * self.retning
        
        # Snu retning hvis den treffer topp eller bunn
        if self.y <= 50 or self.y >= HOYDE - 50:
            self.retning *= -1

    def tegn(self):
        # Tegner kanonløpet pekende mot venstre
        pygame.draw.rect(skjerm, GRA, (self.x - self.lengde, self.y - self.bredde//2, self.lengde, self.bredde))
        # Tegner basen til kanonen
        pygame.draw.circle(skjerm, MORK_GRA, (self.x, self.y), 30)

class Kanon_Kule:
    def __init__(self, x, y, fart):
        self.x, self.y = x, y
        self.radius = 15
        self.fart = fart
        self.offset = random.random() * 10
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius*2, self.radius*2)

    def update(self):
        self.x -= self.fart
        self.y += math.sin(pygame.time.get_ticks() * 0.005 + self.offset) * 2
        self.rect.center = (self.x, self.y)
        

        if pygame.Rect.colliderect(self.rect, spill.spiller.rect):
            spill.running = False
    

    def tegn(self):
        for i in range(8):
            v = i * (math.pi/4) + (pygame.time.get_ticks() * 0.01)
            pygame.draw.line(skjerm, ROD, (self.x, self.y), (self.x + math.cos(v)*22, self.y + math.sin(v)*22), 2)
        
        farge = ROD if (pygame.time.get_ticks() // 200) % 2 == 0 else (50, 0, 0)
        pygame.draw.circle(skjerm, farge, (int(self.x), int(self.y)), self.radius)


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

    def update(self):
        if self.aktiv:
            self.x -= self.fart
            # Hvis den forsvinner ut til venstre

            # Lag rect hver frame
            self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

            if self.x + self.w < 0:
                self.aktiv = False
        else:
            # Sjanse for å dukke opp igjen
            if random.random() < 0.01:
                self._reset()

        # Kollisjonssjekk
        if self.aktiv and pygame.Rect.colliderect(self.rect, spill.spiller.rect):
            spill.running = False


    def tegn(self, skjerm):
        if self.aktiv:
            pygame.draw.rect(skjerm, GRA, (self.x, self.y, self.w, self.h))
            pygame.draw.rect(skjerm, ROD, (self.x, self.y, self.w, self.h), 1)


class Laser(Objecter):
    def __init__(self, x):
        self.x = x
        self.y = random.randint(35, 565)
        self.width = 800
        self.height = 10
        self.rect = pygame.Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)
        self.timer = 0
        self.color = LYSE_ROD

    def update(self):
        # Setter fargen og bredden til rød når timer er mellom 100 og 320
        if self.timer>100 and self.timer <320:
            self.color = ROD
            self.height = 35
        # Hvis ikke skal den være lyse rød og tynn
        else: 
            self.color = LYSE_ROD
            self.height = 10

        self.timer += 1
    
        # Hvert 7 sekund flytter den laseren og nulstiller timeren
        if self.timer >= 420:  # 7 sekunder
            self.y = random.randint(35, 565)
            self.timer = 0

        # Setter at den kun koliderer når laseren er rød
        if pygame.Rect.colliderect(self.rect, spill.spiller.rect):
            if self.color == ROD:
                spill.running = False
            pass

        self.rect = pygame.Rect(
            self.x - self.width // 2,
            self.y - self.height // 2,
            self.width,
            self.height
    )

    def tegn(self):
        pygame.draw.rect(skjerm, self.color, self.rect)




spill = FlippJack()
while spill.running:
    spill.main_loop()