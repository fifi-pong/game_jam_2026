import pygame, random, math, sys

# 1. Oppsett
class FlippJack:
    def __init__(self):
        pygame.init()
        self.skjerm = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.keys = pygame.key.get_pressed()
        self.running = True

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
        self.clock.tick(60)

    def render(self):
        self.skjerm.fill("white")
        pygame.display.flip()
    
#gjennerel oppsett
class Objecter:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = (100, 100, 100)
        self.rect = pygame.Rect(x - width // 2, y - height // 2, width, height)

    def update(self):
        pass

    def render(self):
        pass


class Spiller(Objecter):
    def __init__(self):
        super().__init__()
        pass

class Laser(Objecter):
    def __init__(self):
        super().__init__()
        pass

class Kanon(Objecter):
    def __init__(self):
        super().__init__()
        pass

class Vegger(Objecter):
    def __init__(self):
        super().__init__()
        pass

spill = FlippJack()
while spill.running:
    spill.main_loop()