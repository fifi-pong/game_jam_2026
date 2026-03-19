import pygame, random, math
import FlippJack_main

class Partikkel:
    def __init__(self, x, y, farge, fart_x=-2):
        self.x, self.y = x, y
        self.liv = random.randint(15, 25)
        self.farge = farge
        self.fart_x = fart_x + random.uniform(-1, 1)
        self.fart_y = random.uniform(-1, 1)

    def oppdater(self):
        self.x += self.fart_x
        self.y += self.fart_y
        self.liv -= 1

    def tegn(self):
        if self.liv > 0:
            str_str = max(1, self.liv // 5)
            pygame.draw.circle(skjerm, self.farge, (int(self.x), int(self.y)), str_str)

class Romskip:
    def __init__(self):
        self.x, self.y = 70, 300
        self.fart_y = 0
        self.bredde, self.hoyde = 45, 22
        self.rect = pygame.Rect(self.x, self.y, self.bredde, self.hoyde)
        self.klapp = 0 
        self.partikler = []

    def oppdater(self, hopp):
        self.fart_y += 0.4
        if hopp:
            self.fart_y = -7
            self.klapp = 22 
            for _ in range(8):
                self.partikler.append(Partikkel(self.x, self.y + 11, random.choice([CYAN, GUL, HVIT])))
        
        self.y += self.fart_y
        self.rect.y = self.y
        if self.klapp > 0: self.klapp -= 1.2
        
        for p in self.partikler[:]:
            p.oppdater()
            if p.liv <= 0: self.partikler.remove(p)

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

class Port:
    def __init__(self, x, fart):
        self.x = x
        self.bredde = 85
        self.aapning_y = random.randint(120, 280)
        self.gap = 205 
        self.fart = fart
        self.passert = False
        self.puls = 0
        
        # Variasjon i rom-arkitektur
        self.modul_type = random.choice(["batteri", "sensor", "skrog"])
        self.topp_rect = pygame.Rect(self.x, 0, self.bredde, self.aapning_y)
        self.bunn_rect = pygame.Rect(self.x, self.aapning_y + self.gap, self.bredde, HOYDE)

    def oppdater(self):
        self.x -= self.fart
        self.topp_rect.x = self.x
        self.bunn_rect.x = self.x
        self.puls += 0.05

    def tegn(self):
        lx = self.x + self.bredde // 2
        
        for er_topp in [True, False]:
            y_base = 0 if er_topp else HOYDE
            y_spiss = self.aapning_y if er_topp else self.aapning_y + self.gap
            h = abs(y_spiss - y_base)
            r = 1 if er_topp else -1

            # 1. YTTERSKROG (Deep Space Grey)
            # Vi lager en trapesform for å simulere perspektiv på romstasjonen
            skrog_pts = [
                (self.x - 10, y_base),
                (self.x + self.bredde + 10, y_base),
                (self.x + self.bredde, y_spiss - (15 * r)),
                (self.x, y_spiss - (15 * r))
            ]
            pygame.draw.polygon(skjerm, (25, 25, 35), skrog_pts)
            pygame.draw.polygon(skjerm, (50, 55, 70), skrog_pts, 2)

            # 2. GREEBLES (Mekaniske detaljer inni skroget)
            for i in range(1, 4):
                gy = y_base + (h * (i/4))
                # Små mørke kasser og ledninger
                pygame.draw.rect(skjerm, (15, 15, 20), (self.x + 10, gy, self.bredde - 20, 15))
                pygame.draw.line(skjerm, (40, 40, 50), (self.x + 5, gy), (self.x + self.bredde - 5, gy), 1)

            # 3. NAVIGASJONSLYS (Blinkende LED-lys som på ekte romskip)
            blink = abs(math.sin(self.puls * 2))
            # Grønt/Rødt posisjonslys ytterst på kanten
            lys_farge = (0, 255 * blink, 100 * blink) if er_topp else (255 * blink, 0, 50 * blink)
            pygame.draw.circle(skjerm, lys_farge, (int(self.x - 5), int(y_spiss - (25 * r))), 3)
            pygame.draw.circle(skjerm, (255, 255, 255), (int(self.x - 5), int(y_spiss - (25 * r))), 1)

            # 4. ION-REAKTOR (Den blå glødende kjernen som mater laseren)
            ion_glod = (0, 150 + int(100 * math.sin(self.puls)), 255)
            pygame.draw.rect(skjerm, (0, 20, 40), (lx - 12, y_spiss - (40 * r), 24, 30), 0, 5)
            pygame.draw.rect(skjerm, ion_glod, (lx - 8, y_spiss - (35 * r), 16, 20), 0, 3)

        # 5. ZERO-G LASER (Plasma-stråle med atmosfærisk forstyrrelse)
        # Lagvis glød for å simulere ekstrem varme i vakuum
        for i in range(3):
            b = 10 - i*3
            alpha = 100 - i*30
            s = pygame.Surface((b, self.gap), pygame.SRCALPHA)
            pygame.draw.rect(s, (0, 200, 255, alpha), (0, 0, b, self.gap))
            skjerm.blit(s, (lx - b // 2, self.aapning_y))
            
        # Selve strålekjernen
        pygame.draw.line(skjerm, HVIT, (lx, self.aapning_y), (lx, self.aapning_y + self.gap), 2)
        
        # Energi-partikler som suges mot laseren (Space dust/Plasma)
        if random.random() > 0.7:
            px = lx + random.randint(-15, 15)
            py = self.aapning_y + random.randint(0, self.gap)
            pygame.draw.line(skjerm, CYAN, (px, py), (lx, py), 1)