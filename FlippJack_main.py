import pygame, random, math, sys

# --- Initialisering og farger ---
pygame.init()
BREDDE, HOYDE = 800, 600
skjerm = pygame.display.set_mode((BREDDE, HOYDE))
pygame.display.set_caption("FlippJack - Full Grafikk")
clock = pygame.time.Clock()

MORK_BLA    = (5, 5, 20)
HVIT        = (255, 255, 255)
GRA         = (150, 150, 150)
MORK_GRA    = (60, 60, 60)
CYAN        = (0, 255, 255)
GUL         = (255, 230, 0)
ORANSJE     = (255, 120, 0)
ROD         = (255, 30, 30)
LYSE_ROD    = (247, 64, 64)
PLASM_BLA   = (0, 150, 255)
RAKETT_MORK = (30, 30, 40)

font_stor = pygame.font.SysFont("Arial", 26, bold=True)


class Objecter:
    def __init__(self, x, y, bredde, hoyde):
        self.x = x
        self.y = y
        self.bredde = bredde
        self.hoyde = hoyde
        self.rect = pygame.Rect(x, y, bredde, hoyde)

class Romskip(Objecter):
    def __init__(self, x, y):
        super().__init__(x, y, 46, 22)
        self.fart_x = 0
        self.fart_y = 0

    def update(self, opp, ned, venstre, hoyre):
        acc = 0.5
        friksjon = 0.95
        self.fart_y += 0.2  # Tyngdekraft

        if opp: self.fart_y -= acc
        if ned: self.fart_y += acc
        if venstre: self.fart_x -= acc
        if hoyre: self.fart_x += acc

        self.fart_x *= friksjon
        self.fart_y *= friksjon

        self.x += self.fart_x
        self.y += self.fart_y

        self.x = max(0, min(self.x, BREDDE - self.bredde))
        self.y = max(0, min(self.y, HOYDE - self.hoyde))
        self.rect.topleft = (self.x, self.y)

    def tegn(self):
        # 1. Plasma-flamme (Motor)
        if self.fart_y < 3:
            f_size = random.randint(20, 35) if self.fart_y < 0 else random.randint(10, 20)
            pygame.draw.polygon(skjerm, PLASM_BLA, [(self.x+2, self.y+6), (self.x-f_size, self.y+11), (self.x+2, self.y+16)])
            pygame.draw.polygon(skjerm, HVIT, [(self.x+2, self.y+9), (self.x-f_size//2, self.y+11), (self.x+2, self.y+13)])

        # 2. Vinger
        for v_dir in [-1, 1]:
            v_offset = (self.y + 11) + (v_dir * 4)
            p_liste = [(self.x+20, v_offset), (self.x-12, v_offset + (v_dir*18)), (self.x+5, v_offset)]
            pygame.draw.polygon(skjerm, MORK_GRA, p_liste)
            pygame.draw.polygon(skjerm, GRA, p_liste, 1)

        # 3. Skrog
        kropp = [(self.x, self.y+6), (self.x+35, self.y+3), (self.x+46, self.y+11), (self.x+35, self.y+19), (self.x, self.y+16)]
        pygame.draw.polygon(skjerm, (80, 80, 90), kropp)
        pygame.draw.polygon(skjerm, (40, 40, 50), kropp, 2)
        
        # 4. Cockpit
        vindu = [(self.x+22, self.y+7), (self.x+34, self.y+7), (self.x+40, self.y+11), (self.x+34, self.y+15), (self.x+22, self.y+15)]
        pygame.draw.polygon(skjerm, (0, 60, 100), vindu)
        pygame.draw.polygon(skjerm, CYAN, vindu, 1)

class Kanon:
    def __init__(self, x):
        self.x = x
        self.y = HOYDE // 2
        self.fart = 2           
        self.retning = 1        

    def update(self):
        self.y += self.fart * self.retning
        if self.y <= 80 or self.y >= HOYDE - 80:
            self.retning *= -1

    def tegn(self):
        # Kanonløp
        pygame.draw.rect(skjerm, MORK_GRA, (self.x - 40, self.y - 18, 40, 36))
        pygame.draw.rect(skjerm, GRA, (self.x - 70, self.y - 12, 35, 24))
        pygame.draw.rect(skjerm, (80, 80, 80), (self.x - 75, self.y - 15, 5, 30))
        # Base
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
        self.rect = pygame.Rect(x, y, self.lengde, self.bredde)

    def update(self):
        self.x -= self.fart
        self.y += math.sin(pygame.time.get_ticks() * 0.005 + self.offset) * 2
        self.rect.topleft = (self.x, self.y - self.bredde//2)

    def tegn(self):
        # Flamme bak
        f_str = random.randint(10, 18)
        flamme_x = self.x + self.lengde // 2
        pygame.draw.polygon(skjerm, ORANSJE, [(flamme_x, self.y), (flamme_x + f_str, self.y - 5), (flamme_x + f_str + 3, self.y), (flamme_x + f_str, self.y + 5)])
        pygame.draw.circle(skjerm, GUL, (int(flamme_x + 3), int(self.y)), 3)

        # Boomerang-kropp
        punkter = [
            (self.x, self.y),
            (self.x + self.lengde // 2, self.y - self.bredde // 2),
            (self.x + self.lengde, self.y - self.bredde // 4),
            (self.x + self.lengde // 2, self.y),
            (self.x + self.lengde, self.y + self.bredde // 4),
            (self.x + self.lengde // 2, self.y + self.bredde // 2),
        ]
        pygame.draw.polygon(skjerm, RAKETT_MORK, punkter)
        pygame.draw.polygon(skjerm, ROD, punkter, 2)

class Vegg:
    def __init__(self):
        self.w = 12
        self.aktiv = False
        self._reset()

    def _reset(self):
        self.x = BREDDE + 50
        self.h = random.randint(100, 250)
        self.y = random.randint(50, HOYDE - self.h - 50)
        self.fart = random.randint(2, 4)
        self.aktiv = True
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def update(self):
        if self.aktiv:
            self.x -= self.fart
            self.rect.topleft = (self.x, self.y)
            if self.x + self.w < 0: self.aktiv = False
        elif random.random() < 0.01:
            self._reset()

    def tegn(self):
        if self.aktiv:
            pygame.draw.rect(skjerm, GRA, self.rect)
            pygame.draw.rect(skjerm, ROD, self.rect, 1)

class Laser:
    def __init__(self):
        self.y = random.randint(50, 550)
        self.timer = 0
        self.height = 2
        self.color = LYSE_ROD
        self.rect = pygame.Rect(0, self.y, BREDDE, self.height)

    def update(self):
        self.timer += 1
        if 100 < self.timer < 320:
            self.color = ROD
            self.height = 35
        else:
            self.color = LYSE_ROD
            self.height = 4 if self.timer % 10 < 5 else 2
            
        if self.timer >= 420:
            self.y = random.randint(50, 550)
            self.timer = 0
            
        self.rect = pygame.Rect(0, self.y - self.height // 2, BREDDE, self.height)

    def tegn(self):
        if self.color == ROD:
            # Glødende effekt
            pygame.draw.rect(skjerm, ORANSJE, (0, self.rect.y - 2, BREDDE, self.rect.height + 4))
            pygame.draw.rect(skjerm, self.color, self.rect)
            pygame.draw.rect(skjerm, HVIT, (0, self.rect.y + self.height//3, BREDDE, self.height//3))
            # Gnister
            for _ in range(3):
                gx = random.randint(0, BREDDE)
                pygame.draw.line(skjerm, CYAN, (gx, self.y-10), (gx+10, self.y+10), 1)
        else:
            pygame.draw.rect(skjerm, self.color, self.rect)

class FlippJack:
    def __init__(self):
        self.running = True
        self.spiller = Romskip(70, 300)
        self.kanon = Kanon(BREDDE - 10)
        self.kuler = []
        self.skyt_timer = 0
        self.laser = Laser()
        self.vegg = Vegg()
        self.poeng = 0
        self.keys = pygame.key.get_pressed()

    def update(self):
        dt = clock.tick(60) / 1000
        self.poeng += dt
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False
        self.keys = pygame.key.get_pressed()

        # Oppdateringer
        self.spiller.update(self.keys[pygame.K_UP], self.keys[pygame.K_DOWN], self.keys[pygame.K_LEFT], self.keys[pygame.K_RIGHT])
        self.kanon.update()
        self.laser.update()
        self.vegg.update()

        # Skyting
        self.skyt_timer += clock.get_time()
        if self.skyt_timer >= 850:
            self.kuler.append(BoomerangRakett(self.kanon.x - 75, self.kanon.y, random.randint(5, 8)))
            self.skyt_timer = 0

        # Kollisjonssjekker
        for kule in self.kuler[:]:
            kule.update()
            if kule.rect.colliderect(self.spiller.rect): self.running = False
            if kule.x < -100: self.kuler.remove(kule)

        if self.laser.color == ROD and self.laser.rect.colliderect(self.spiller.rect): self.running = False
        if self.vegg.aktiv and self.vegg.rect.colliderect(self.spiller.rect): self.running = False

    def render(self):
        skjerm.fill(MORK_BLA)
        self.vegg.tegn()
        for kule in self.kuler: kule.tegn()
        self.kanon.tegn()
        self.laser.tegn()
        self.spiller.tegn()
        
        score_text = font_stor.render(f"SCORE: {int(self.poeng)}", True, HVIT)
        skjerm.blit(score_text, (BREDDE//2 - 40, 20))
        pygame.display.flip()

spill = FlippJack()
while spill.running:
    spill.update()
    spill.render()
pygame.quit()