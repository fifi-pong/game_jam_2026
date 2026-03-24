import pygame, random, math
import FlippJack_main

# --- OPPSETT OG FARGER ---
pygame.init()
BREDDE, HOYDE = 800, 600
skjerm = pygame.display.set_mode((BREDDE, HOYDE))
klokke = pygame.time.Clock()

# --- FARGER ---
MORK_BLA    = (5, 5, 20)
HVIT        = (255, 255, 255)
GRA         = (150, 150, 150)
MORK_GRA    = (60, 60, 60)
CYAN        = (0, 255, 255)
GUL         = (255, 255, 0)
ORANSJE     = (255, 100, 0)
ROD         = (255, 30, 30)
NEON_LILLA  = (180, 0, 255)
PLASM_BLA   = (0, 150, 255)

class Romskip():
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