import pygame, random, math

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
        # Aktiv laserfase (Timer 100 til 320)
        if 100 < self.timer < 320:
            self.color = ROD
            self.height = 35
        else: 
            # Advarselsfase: Flimrer raskere jo nærmere den er aktivering
            self.color = LYSE_ROD
            self.height = 4 if self.timer % 10 < 5 else 2 # Flimre-effekt
            
        self.timer += 1
    
        # Reset etter 7 sekunder (420 frames)
        if self.timer >= 420:
            self.y = random.randint(35, 565)
            self.timer = 0

        # Kollisjonssjekk kun når laseren er tykk/farlig
        self.rect = pygame.Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)
        if self.color == ROD and self.rect.colliderect(spill.spiller.rect):
            spill.running = False

    def tegn(self):
        if self.color == ROD:
            # Hovedstråle (ytre glød)
            pygame.draw.rect(skjerm, ORANSJE, (self.rect.x, self.rect.y - 2, self.rect.width, self.rect.height + 4))
            pygame.draw.rect(skjerm, self.color, self.rect)
            # Indre kjerne (hvitglødende senter)
            pygame.draw.rect(skjerm, HVIT, (self.rect.x, self.rect.y + self.height//3, self.rect.width, self.height//3))
            
            # Legger til små "elektriske" gnister langs laseren
            for _ in range(5):
                gx = random.randint(0, BREDDE)
                gy = self.y + random.randint(-20, 20)
                pygame.draw.line(skjerm, CYAN, (gx, gy), (gx + 10, gy), 2)
        else:
            # Tegner den tynne advarselslinjen
            pygame.draw.rect(skjerm, self.color, self.rect)