import pyxel
import util as util

class Hero:
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
            (self.x + 14, self.y + 2),
            (self.x + 2, self.y + 14),
            (self.x + 14, self.y + 14),
        )

    def update(self):
        self.age += 1
        if util.rectangles_overlap(self.hit(), self.game.tobo2.hit()):
            self.game.tobo2.revealed()

    def draw(self):
        u = 80
        v = 16 + (16 * (0, 1, 0, 1, 0, 0, 0, 0)[self.age % 8])
        pyxel.blt(self.x, self.y, 0, u, v, 16 * self.direction, 16, 0)
