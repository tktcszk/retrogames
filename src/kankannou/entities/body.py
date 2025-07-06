import pyxel


class Body:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.arms_degree = [0, 0, 0, 0]

    def update(self):
        for idx, d in enumerate(self.arms_degree):
            self.arms_degree[idx] = (d + 15) % 360

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 16, 8, 16, 0)

        # arm right
        pyxel.blt(self.x + 8 - 4, self.y + 8 - 3, 0, 8, 24, 8, 8, 0, self.arms_degree[0])
        # arm left
        pyxel.blt(self.x + -8 + 4, self.y + 8 - 3, 0, 8, 24, -8, 8, 0, self.arms_degree[1])

        # leg right
        pyxel.blt(self.x + 2, self.y + 16 - 5, 0, 8, 32, 8, 8, 0, self.arms_degree[2])
        x = pyxel.cos(self.arms_degree[2] + 45) * 4 + 4
        y = pyxel.sin(self.arms_degree[2] + 45) * 4 + 4

        pyxel.pset(self.x + 2 + x, self.y + 16 - 5 + y, 8)
        pyxel.blt(self.x + 2 + x -4, self.y + 16 - 5 + y -4, 0, 8, 32, 8, 8, 0, 45)

        # leg left
        pyxel.blt(self.x + 0, self.y + 16 - 5, 0, 8, 32, -8, 8, 0, self.arms_degree[2])
        x = pyxel.cos(self.arms_degree[3] + 45) * 4 - 4
        y = pyxel.sin(self.arms_degree[3] + 45) * 4 + 4

        pyxel.pset(self.x + 0 + x, self.y + 16 - 5 + y, 8)
        pyxel.blt(self.x + 0 + x -4, self.y + 16 - 5 + y -4, 0, 8, 32, -8, 8, 0, 45)


#        # arm left
#        pyxel.blt(self.x, self.y + 16 - 8, 0, 8, 32, -8, 8, 0, self.arms_degree[0])
