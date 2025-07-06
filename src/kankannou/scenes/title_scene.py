import pyxel
import utils

class TitleScene:
    def __init__(self, game):
        self.game = game

    def start(self):
        pass

    def stop(self):
        pass

    def update(self):
        if pyxel.btnp(pyxel.KEY_UP):
            self.game.subtitle_idx = (self.game.subtitle_idx - 1) % len(self.game.subtitles)
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.game.subtitle_idx = (self.game.subtitle_idx + 1) % len(self.game.subtitles)
        if pyxel.btnp(pyxel.KEY_A):
            self.game.notify(self, "start")

    def draw(self):
        pyxel.cls(0)
        x = self.game.window_width / 2 - len(self.game.title) * 4 / 2
        y = self.game.window_height / 2 - 4
        pyxel.text(x, y, self.game.title, 7)

        offset_y = y + 8

        for idx, subtitle in enumerate(self.game.subtitles):
            _subtitle = ('[*] ' if idx == self.game.subtitle_idx else '[ ] ') + subtitle[0]
            x2 = 60
            y2 = offset_y + (8 * idx)
            pyxel.text(x2, y2, _subtitle, 7)


    