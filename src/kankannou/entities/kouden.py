import pyxel

class Kouden:
    def __init__(self, game, x, y, speed, msc, _type):
        self.game = game
        self.x = x
        self.y = y
        self.speed = speed
        self.msc = msc
        self._type = _type
        self.alive = True

    def update(self):
        self.y = self.y + self.speed
        self.speed += 1

        if self.y > self.game.window_height + 10:
            self.alive = False

    def draw(self):
        x = 8 * self.msc
        y = 48 + self._type * 8
        pyxel.blt(self.x, self.y, 0, x, y, 8, 8, 0)

        