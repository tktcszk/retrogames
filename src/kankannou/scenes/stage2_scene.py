import pyxel
import utils

class Stage2Scene:
    def __init__(self, game):
        self.game = game
        self.subtitle = "OWNER OF THE NAGAYA"

    def start(self):
        pyxel.playm(0)
        pass

    def stop(self):
        pyxel.stop()
        pass

    def update(self):
        btns = utils.keypress()

        if len(btns) > 0:
            self.game.notify(self, "end")


    def draw(self):
        pyxel.cls(0)
        x = self.game.window_width / 2 - len(self.game.title) * 4 / 2
        y = self.game.window_height / 2 - 4
        pyxel.text(x, y, self.game.title, 7)

        x = self.game.window_width / 2 - len(self.subtitle) * 4 / 2
        y = self.game.window_height / 2 + 8
        pyxel.text(x, y, self.subtitle, 7)
