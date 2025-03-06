import pyxel
import math

GAME_TITLE = "PLAYGROUND"
WINDOW_WIDTH = 100
WINDOW_HEIGHT = 100
MODE_TITLE = 1
MODE_PLAYING = 2
MODE_GAMEOVER = 3


def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

class Game:
    def __init__(self):
        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT, title=GAME_TITLE, fps=10)
        pyxel.load("playground.pyxres")
        pyxel.mouse(True)

        self.mode = MODE_TITLE
        self.score = 0
        self.player = Player(50, 50)
    
    def update(self):
        if self.mode == MODE_TITLE:
            if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
                self.mode = MODE_PLAYING
                self.reset_game()
            return
        elif self.mode == MODE_PLAYING:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                mouse_x = pyxel.mouse_x
                mouse_y = pyxel.mouse_y
                d = distance(self.player.x, self.player.y, mouse_x, mouse_y)
                if 0 < d < 4:
                    self.player.bounce = True
                    power = (5.0 / d) ** 2
                    self.player.x2 = self.player.x + ((self.player.x - mouse_x) * power)
                    self.player.y2 = self.player.y + ((self.player.y - mouse_y) * power)
                    #print(self.player.x2, self.player.y2)
            self.player.update()
        elif self.mode == MODE_GAMEOVER:
            if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
                self.mode = MODE_PLAYING
                self.reset_game()
            return

    def draw(self):
        pyxel.cls(0)

        if self.mode == MODE_TITLE:
            self.draw_title()
        elif self.mode == MODE_PLAYING:
            self.draw_playing()
        elif self.mode == MODE_GAMEOVER:
            self.draw_gameover()

    def draw_title(self):
        for i in range(1, -1, -1):
            color = 10 if i == 0 else 8
            title_x = WINDOW_WIDTH / 2 - (len(GAME_TITLE) / 2) * 4
            title_y = WINDOW_HEIGHT / 2 - 2

            pyxel.text(title_x, 20 + i, GAME_TITLE, color)
        message = "- Press UP Key -"
        message_x = WINDOW_WIDTH / 2 - (len(message) / 2) * 4

        pyxel.text(message_x, 40 + i, message, 3)
    
    def draw_playing(self):
        self.player.draw()

    def draw_gameover(self):
        for i in range(1, -1, -1):
            color = 10 if i == 0 else 8
            title_x = WINDOW_WIDTH / 2 - (len(GAME_TITLE) / 2) * 4
            pyxel.text(title_x, 20 + i, GAME_TITLE, color)

        message = "GAME OVER"
        message_x = WINDOW_WIDTH / 2 - (len(message) / 2) * 4

        pyxel.text(message_x, 30 + i, message, 2)

        message = "- Press Up Key -"
        message_x = WINDOW_WIDTH / 2 - (len(message) / 2) * 4

        pyxel.text(message_x, 40 + i, message, 3)

    def run(self):
        pyxel.run(self.update, self.draw)

    def reset_game(self):
        self.mode = MODE_PLAYING
        self.score = 0

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.x2 = None
        self.y2 = None
        self.bounce = False
        self.costume = 0

    def update(self):
        self.costume = (self.costume + 1) % 2
        if self.bounce:
            d = distance(self.x, self.y, self.x2, self.y2) 
            print(d)
            if d < 1:
                self.bounce = False
                self.x2 = None
                self.y2 = None
            else:
                self.x += (self.x2 - self.x) / 2
                self.y += (self.y2 - self.y) / 2


    def draw(self):
        pyxel.blt(self.x - 4, self.y - 4, 0, 0, 0 + (self.costume % 2) * 8, 8, 8, 0)

Game().run()

