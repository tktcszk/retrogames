import pyxel
import config
from entities import Fugu, Rakuda, Tobo

class PlayScene:
    def __init__(self, game):
        self.game = game
        self.entities = []
        self.rakuda = Rakuda(self, config.WINDOW_WIDTH / 2, config.WINDOW_WIDTH / 2)
        self.entities.append(self.rakuda)

    def reset(self):
        self.entities = []
        self.rakuda = Rakuda(self, config.WINDOW_WIDTH / 2, config.WINDOW_WIDTH / 2)
        self.entities.append(self.rakuda)

    def start(self):
        self.reset()
        pyxel.playm(0)
        print("play start:")

    def stop(self):
        pyxel.stop()

    def update(self):
        if pyxel.rndi(0,8) == 0:
            fugu = Fugu(self, pyxel.rndi(0, config.WINDOW_WIDTH), pyxel.rndi(0, config.WINDOW_HEIGHT))
            self.entities.append(fugu)

        if pyxel.rndi(0,64) == 0:
            tobo = Tobo(self, pyxel.rndi(0, config.WINDOW_WIDTH), pyxel.rndi(0, config.WINDOW_HEIGHT))
            self.entities.insert(0, tobo)

        entities = []
        for entity in self.entities:
            entity.update()
            if entity.alive:
                entities.append(entity)
        self.entities = entities

        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
            self.rakuda.up()
        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
            self.rakuda.down()
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            self.rakuda.right()
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            self.rakuda.left()
        if pyxel.btnp(pyxel.KEY_A) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
            self.rakuda.knife()

        if not self.rakuda.alive:
            self.game.notify(self, "gameover")

    def draw(self):
        pyxel.cls(0)
        for entity in self.entities:
            entity.draw()

        bar_w = config.WINDOW_WIDTH - 16
        pyxel.rect(8, config.WINDOW_HEIGHT - 16, bar_w, 8, 6)
        if self.rakuda.damage > 0:
            damage = self.rakuda.damage
            c = 10 if damage < 22 else 8
            w = bar_w if damage > 24 else damage * (bar_w / 23)
            offset_x = bar_w - w
            pyxel.rect(8 + offset_x, config.WINDOW_HEIGHT - 16, w, 8, c)
        