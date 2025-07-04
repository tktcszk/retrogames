import pyxel
import util as util
import config

class Tobo:
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.speed = pyxel.rndi(1, 4)
        self.direction = 1
        self.age = 0
        self.eaten = False
        self.cutten = False
        self.decay = 0
        self.alive = True
    
    def hit(self):
        return (
            (self.x + 2, self.y + 2),
            (self.x + 6, self.y + 2),
            (self.x + 2, self.y + 6),
            (self.x + 6, self.y + 6),
        )

    def update(self):
        self.age += 1
        self.x = self.x + self.speed * self.direction
        if not 0 <= self.x < config.WINDOW_WIDTH:
            self.alive = False

    def draw(self):
        u = 48
        v = 16 + (8 * (self.age % 2))
        pyxel.blt(self.x, self.y, 0, u, v, 8 * self.direction, 8, 0)
