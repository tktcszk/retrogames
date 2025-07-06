import pyxel
import config

class StandbyScene:
    def __init__(self, game):
        self.game = game
        self.age = 0
        self.reset()

    def reset(self):
        self.age = 0
        pass

    def start(self):
        self.reset()

    def stop(self):
        pass

    def update(self):
        self.age += 1
        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
            self.game.notify(self, "play")
        if pyxel.btn(pyxel.KEY_A):
            self.game.notify(self, "title")
        return

    def draw(self):
        pyxel.cls(0)

        if self.age > 10:
            message = "STAND BY"
            message_x = config.WINDOW_WIDTH / 2 - (len(message) / 2) * 4

            pyxel.text(message_x, 75, message, 13)

        if self.age > 70:
            message = "- Press Any Key -"
            message_x = config.WINDOW_WIDTH / 2 - (len(message) / 2) * 4
            pyxel.text(message_x, 90, message, 3)
