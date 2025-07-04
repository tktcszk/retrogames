import pyxel
import util as util

class Tobo2:
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
        self._revealed = False
        self.revealed_count = 0

    
    def hit(self):
        return (
            (self.x + 2, self.y + 2),
            (self.x + 14, self.y + 2),
            (self.x + 2, self.y + 14),
            (self.x + 14, self.y + 14),
        )
    
    def revealed(self):
        self._revealed = True
        pyxel.play(3, 63)

    def update(self):
        self.age += 1

        if self._revealed:
            self.revealed_count += 1

    def draw(self):
        u = 64
        v = 64

        if self._revealed:
            v1 = 16 + (16 * (0, 1, 2, 1, 0, 0, 0, 0)[self.age % 8])
            pyxel.blt(self.x, self.y, 0, u, v1, 16 * self.direction, 16, 0)
            if self.revealed_count < 8:
                v2 = 64 + (16 * (0, 1, 2, 1, 2, 3, 3, 3)[self.revealed_count])
                pyxel.blt(self.x, self.y, 0, u, v2, 16 * self.direction, 16, 0)
        else:
            pyxel.blt(self.x, self.y, 0, u, v, 16, 16, 0)

