"""
Dette er staten for spillet. Det er her du legger til Spillobjekter, logikk, etc...
"""

from states.base_state import BaseState
import pygame, random, math, sys

pygame.init()
BREDDE, HOYDE = 800, 600
skjerm = pygame.display.set_mode((BREDDE, HOYDE))
pygame.display.set_caption("FlippJack")
clock = pygame.time.Clock()


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
RAKETT_MORK = (30, 30, 40)

font_stor = pygame.font.SysFont("Arial", 26, bold=True)
font_liten = pygame.font.SysFont("Arial", 16, bold=True)

class GameState(BaseState):
    def __init__(self):
        super().__init__()
        self.keys = pygame.key.get_pressed()
        self.running = True
        self.kanon = Kanon(BREDDE - 10)
        self.kuler = []
        self.skyt_timer = 0
        self.vegg = Vegg()
        self.laser = Laser()
        self.totaltid = 0

        self.spiller = Romskip(70, 300)

        self.poeng = 0

        self.skjold_tid = 0
        self.powerup_timer = 0
        self.bonuser = []
        self.neste_powerup = random.uniform(5, 10)  # mellom 5–10 sek

        try:
            self.bakgrunn_img = pygame.image.load("pix_art.jpg").convert()
            self.bakgrunn = pygame.transform.scale(self.bakgrunn_img, (BREDDE, HOYDE))
        except:
            # Fallback hvis filen mangler
            self.bakgrunn = pygame.Surface((BREDDE, HOYDE))
            self.bakgrunn.fill(MORK_BLA)

    def handle_events(self, events : list[pygame.event.Event]):
        for event in events:
            if event.type == pygame.QUIT:
                self.next_state = None
                self.done = True
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.next_state = "MENU"
                    self.done = True
            self.keys = pygame.key.get_pressed()

    def update(self, dt: float):
        if self.skjold_tid > 0: self.skjold_tid -= 1
        spill_fart = 3 + (self.poeng // 5) * 0.4
        dt = clock.tick(60) / 1000
        self.poeng += dt
        #spilleren
        opp = self.keys[pygame.K_UP]
        ned = self.keys[pygame.K_DOWN]
        venstre = self.keys[pygame.K_LEFT]
        hoyre = self.keys[pygame.K_RIGHT]

        #opptatering
        self.spiller.update(opp, ned, venstre, hoyre)
        self.kanon.update()
        self.vegg.update()
        self.laser.update()

        # Skyting
        self.skyt_timer += clock.get_time()
        if self.skyt_timer >= 850:
            self.kuler.append(BoomerangRakett(self.kanon.x - 75, self.kanon.y, random.randint(5, 8)))
            self.skyt_timer = 0

        # Power up
        self.powerup_timer += dt

        if self.powerup_timer >= self.neste_powerup:
            self.bonuser.append(PowerUp(BREDDE + 50, spill_fart))
            self.powerup_timer = 0
            self.neste_powerup = random.uniform(5, 10)
        


        # Kollisjonssjekker
        for b in self.bonuser[:]:
            b.oppdater()
            if self.spiller.rect.colliderect(b.rect): self.skjold_tid = 180; self.bonuser.remove(b)
            elif b.x < -100: self.bonuser.remove(b)

        for kule in self.kuler[:]:
            kule.update()
            if kule.rect.colliderect(self.spiller.rect):
                if self.skjold_tid <= 0:
                    self.running = False
            if kule.x < -100: self.kuler.remove(kule)

        if self.vegg.aktiv and self.vegg.rect.colliderect(self.spiller.rect): 
                if self.skjold_tid <= 0:
                    self.running = False
        if self.laser.color == ROD and self.laser.rect.colliderect(self.spiller.rect): 
            if self.skjold_tid <= 0:
                self.running = False
    


        if not self.running:
            self.__init__()
            self.done = True
            self.next_state = "MENU"


    def draw(self, skjerm):
        # 1. Tegn bakgrunnen først
        skjerm.blit(self.bakgrunn, (0, 0))

        for b in self.bonuser: b.tegn()
        self.laser.tegn()
        self.vegg.tegn()
        self.spiller.tegn(self.skjold_tid > 0)
        for kule in self.kuler: kule.tegn()
        self.kanon.tegn()

        score_text = font_stor.render(f"SCORE: {int(self.poeng)}", True, HVIT)
        skjerm.blit(score_text, (BREDDE//2 - 40, 20))

        pygame.display.flip()
        

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
        pygame.draw.circle(skjerm, (80, 80, 80), (self.x, self.y), 35)
        pygame.draw.circle(skjerm, GRA, (self.x, self.y), 30)
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
            pygame.draw.rect(skjerm, ORANSJE, (0, self.rect.y - 2, BREDDE, self.rect.height + 4))
            pygame.draw.rect(skjerm, self.color, self.rect)
            pygame.draw.rect(skjerm, HVIT, (0, self.rect.y + self.height//3, BREDDE, self.height//3))
            for _ in range(3):
                gx = random.randint(0, BREDDE)
                pygame.draw.line(skjerm, CYAN, (gx, self.y-10), (gx+10, self.y+10), 1)
        else:
            pygame.draw.rect(skjerm, self.color, self.rect)

class PowerUp:
    def __init__(self, x, fart):
        self.x, self.y = x, random.randint(150, 450)
        self.fart = 3
        self.rect = pygame.Rect(self.x - 10, self.y - 10, 20, 20)

    def oppdater(self):
        self.x -= self.fart
        self.rect.x = self.x

    def tegn(self):
        v = pygame.time.get_ticks() * 0.005
        s = 12 + math.sin(v) * 3
        pygame.draw.rect(skjerm, (0, 255, 100), (self.x - s, self.y - s, s*2, s*2), 2)
        pygame.draw.line(skjerm, HVIT, (self.x-6, self.y), (self.x+6, self.y), 3)
        pygame.draw.line(skjerm, HVIT, (self.x, self.y-6), (self.x, self.y+6), 3)