import pyxel
import utils
from entities import Body, Kouden

class SongScene:
    def __init__(self, game, msc):
        self.game = game
        self.commands = [
            "back to title",
            'stop',
            'start'
        ]
        self.command_idx = 0
        self.msc = msc

        self.entities = []

    def start(self):
        pyxel.playm(self.msc, loop=False)

    def stop(self):
        pyxel.stop()

    def update(self):
        if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
            self.command_idx = (self.command_idx - 1) % len(self.commands)
        if pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
            self.command_idx = (self.command_idx + 1) % len(self.commands)
        if pyxel.btnp(pyxel.KEY_A) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
            if self.commands[self.command_idx] == "back to title":
                self.game.notify(self, "title")
            elif self.commands[self.command_idx] == "stop":
                self.stop()
            elif self.commands[self.command_idx] == "start":
                self.start()

        if pyxel.rndi(0, 16) == 0:
            self.entities.append(Kouden(self.game, pyxel.rndi(0, self.game.window_width), 0, pyxel.rndi(1,2), self.msc, pyxel.rndi(0,5)))

        entities = []
        for entity in self.entities:
            entity.update()
            if entity.alive:
                entities.append(entity)

        self.entities = entities

        return

    def draw(self):
        pyxel.cls(0)

        for entity in self.entities:
            entity.draw()

        x = self.game.window_width / 2 - len(self.game.title) * 4 / 2
        y = self.game.window_height / 2 - 4
        pyxel.text(x, y, self.game.title, 7)

        pyxel.text(60, y + 8, self.game.get_current_subtitle(), 7)

        offset_y = y + 16
        for idx, command in enumerate(self.commands):
            pyxel.text(60, offset_y + idx * 8, ('[*] ' if idx==self.command_idx else '[ ] ') + command, 7)


        
