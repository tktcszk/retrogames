import pyxel
import util as util

class Fugu:
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
        if not self.eaten and not self.cutten:
            (x, y) = (self.game.rakuda.x, self.game.rakuda.y)
            deg = pyxel.atan2(y - self.y, x - self.x)
            self.x = self.x + pyxel.cos(deg) * self.speed
            self.y = self.y + pyxel.sin(deg) * self.speed
            if -90 <= deg < 90:
                self.direction = 1
            else:
                self.direction = -1

            if util.rectangles_overlap(self.hit(), self.game.rakuda.cut()):
                self.cutten = True
                self.decay = pyxel.rndi(1, 4)
            elif util.rectangles_overlap(self.hit(), self.game.rakuda.hit()):
                self.game.rakuda.eat(self)
                self.eaten = True
                self.decay = pyxel.rndi(1, 4)
        else:
            self.decay -= 1
            if self.decay == 0:
                self.alive = False

    def draw(self):
        if not self.eaten:
            if not self.cutten:
                u = 8 * (self.age % 2)
                v = 16 + (8 * (self.age % 7))
                pyxel.blt(self.x, self.y, 0, u, v, 8 * self.direction, 8, 0)
            else:
                u = 8 * (self.age % 2)
                pyxel.blt(self.x, self.y, 0, u, 72, 8 * self.direction, 8, 0)

        else:
            r = pyxel.rndi(2,5)
            pyxel.circb(self.x + r, self.y + r, r, pyxel.rndi(0, 15))
