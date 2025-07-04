import pyxel

class Rakuda:
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.age = 0
        self.points = []
        self.alive = True
        self.damage = 0
        self.speed = 4
        self.dead_count = 0
        self.knife_count = 0

    def eat(self, fugu):
        self.damage += fugu.speed
        pyxel.play(3, 61)

    def hit(self):
        return (
            (self.x + 2, self.y + 2),
            (self.x + 6, self.y + 2),
            (self.x + 2, self.y + 6),
            (self.x + 6, self.y + 6),
        )
    
    def cut(self):
        if self.knife_count > 0:

            return (
                (self.x - 4, self.y + 1),
                (self.x + 12, self.y + 1),
                (self.x + 12, self.y + 7),
                (self.x - 4, self.y + 7),
            )
        else:
            return (
                (self.x - 4, self.y - 10),
                (self.x - 2, self.y - 10),
                (self.x - 2, self.y - 14),
                (self.x - 4, self.y - 14),
            )

    def move2(self, x, y):
        self.x = self.x + self.speed * x
        self.y = self.y + self.speed * y

    def up(self):
        self.move2(0, -1)

    def down(self):
        self.move2(0, 1)

    def right(self):
        self.move2(1, 0)
        self.direction = 1

    def left(self):
        self.move2(-1, 0)
        self.direction = -1

    def knife(self):
        self.knife_count = 8

    def update(self):
        self.age += 1
        damage_level = self.damage // 4
        if damage_level >= 6:
            self.dead_count += 1
        if self.dead_count > 6:
            self.alive = False
        if self.knife_count > 0:
            self.knife_count -= 1

    def draw(self):
        # mage
        pyxel.pset(self.x + 4, self.y - 1, 4)

        # head
        u = 16
        damage_level = min(self.damage // 4, 6)
        v = 16 + (8 * damage_level)
        pyxel.blt(self.x, self.y, 0, u, v, 8, 8, 0)

        # body
        pyxel.blt(self.x, self.y + 8 , 0, 24, 16, 8, 8, 0)

        # arms
        if self.knife_count != 0:
            offset_x = 32
            offset_y = 40
            degree = 45 * self.knife_count
            pyxel.blt(self.x - 8, self.y, 0, offset_x, offset_y, 16, 16, 0, degree)
            pyxel.blt(self.x + 7, self.y + 1, 0, 40, 32, 8, 8, 0)

            degree2 = 45 * (self.knife_count - 1)

            pyxel.line(
                self.x + pyxel.cos(degree) + 8, self.y + 8 + pyxel.sin(degree),
                self.x + pyxel.cos(degree2) + 8, self.y + 8 + pyxel.sin(degree2),
                7)


        else:
            v = 16 + (8 * (self.age % 2))
            pyxel.blt(self.x - 8, self.y + 8 , 0, 32, v, 8, 8, 0)
            pyxel.blt(self.x + 8, self.y + 8 , 0, 40, v, 8, 8, 0)

        # legs
        v = 24 + 8 * [0,1,0,2][self.age % 4]
        pyxel.blt(self.x, self.y + 16 , 0, 24, v, 8, 8, 0)

