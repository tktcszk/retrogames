import pyxel

class TitleScene:
    def __init__(self, game):
        self.game = game
        pass

    def update(self):
        pass

    def draw(self):
        x = self.game.window_width / 2 - (len(self.game.title) * 4 / 2)
        y = self.game.window_width / 2 - 4
        pyxel.text(x, y, self.game.title, 7)
        