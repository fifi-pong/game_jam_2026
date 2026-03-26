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