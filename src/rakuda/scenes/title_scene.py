import pyxel
import config

class TitleScene:
    def __init__(self, game):
        self.game = game
        self.age = 0
        self.logo_y = -20
        self.reset()

    def reset(self):
        self.age = 0
        self.logo_y = -20
        self.standby = True

    def start(self):
        self.reset()
        pyxel.playm(2)

    def stop(self):
        pyxel.stop()

    def update(self):
        self.age += 1
        if self.logo_y < 15:
            self.logo_y += 1

        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
            self.game.notify(self, "keypress")
        return

    def draw(self):
        pyxel.cls(0)
        pyxel.blt(0, self.logo_y, self.game.title_logo, 0, 0, self.game.title_logo.width, self.game.title_logo.height)

        if self.age > 30:
            for i in range(1, -1, -1):
                color = 10 if i == 0 else 8
                title_x = config.WINDOW_WIDTH / 2 - (len(config.TITLE) / 2) * 10
                pyxel.text(title_x, 60 + i, config.TITLE, color, self.game.font)

        if self.age > 50:
            message = "DANCE WITH RAKUDA'S BODY"
            message_x = config.WINDOW_WIDTH / 2 - (len(message) / 2) * 4

            pyxel.text(message_x, 75, message, 13)

        if self.age > 70:
            message = "- Press Any Key -"
            message_x = config.WINDOW_WIDTH / 2 - (len(message) / 2) * 4
            pyxel.text(message_x, 90, message, 3)
