import pyxel
import math

GAME_TITLE = "SUSHI"
WINDOW_WIDTH = 100
WINDOW_HEIGHT = 100
INITIAL_COUNT = 4
MENU = {
    1: "Saba",
    2: "Maguro",
    3: "Gunkan",
}

def cmp(a, b):
    if a == b:
        return 0
    else:
        return 1 if a - b > 0 else -1


def bit(v, flg):
    return 1 if v & flg == flg else 0


def distance(a, b):
    return math.sqrt((b.x - a.x) ** 2 + (b.y - a.y) ** 2)


def direction(a, b, leave=False):
    return cmp(a.x, b.x) * (-1 if leave else 1), cmp(a.y, b.y) * (-1 if leave else 1)


def is_overlapping(a, b):
    x_overlap = a.x <= b.x <= a.x + a.size or a.x < b.x + b.size <= a.x + a.size
    y_overlap = a.y <= b.y <= a.y + a.size or a.y < b.y + b.size <= a.y + a.size

    return x_overlap and y_overlap


class SushiGame:
    def __init__(self):
        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT, title=GAME_TITLE, fps=10)
        pyxel.load("sushi.pyxres")
        self.init_sound()
        self.is_title = True
        self.is_gameover = False
        self.sushi_list = []
        self.messages = []
        self.player = None
        self.score = 0
        self.hit = False
        self.reset_game()

        pyxel.run(self.update, self.draw)

    def init_sound(self):
        # Set sound effects
        pyxel.sounds[0].set("a3a2c1a1", "p", "7", "s", 5)
        pyxel.sounds[1].set("f3e2a1a1", "n", "7742", "s", 10)

    def reset_game(self):
        self.player = Player(self, WINDOW_WIDTH / 2 - 2, WINDOW_HEIGHT / 2 - 2)
        self.sushi_list = [Sushi(self) for i in range(INITIAL_COUNT)]
        self.score = 0

    def update(self):
        if self.hit  > 0:
            self.hit -= 1

        if self.is_title or self.is_gameover:
            if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
                self.is_title = False
                self.is_gameover = False
                self.reset_game()
            return
        else:
            if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
                self.player.up()
            if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
                self.player.down()
            if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(
                pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT
            ):
                self.player.right()
            if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
                self.player.left()

            if pyxel.btnp(pyxel.KEY_A) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                self.player.speedup(True)
            else:
                self.player.speedup(False)

        self.player.update()

        for sushi in self.sushi_list:
            sushi.update()

        self.sushi_list = [sushi for sushi in self.sushi_list if sushi.alive]

        for sushi in self.sushi_list:
            if is_overlapping(self.player, sushi):
                if sushi.spoiled:
                    pyxel.play(1, 1)
                    self.player.refresh()
                    sushi.alive = False
                    self.hit = 5
                    self.messages.append(Message("Agari", sushi.x, sushi.y))
                    break
                else:
                    if self.player.enough:
                        pass
                    else:
                        self.score += 1
                        self.player.eat()
                        self.messages.append(Message(MENU[sushi.menu], sushi.x, sushi.y, 4))
                        pyxel.play(0, 1)
                        sushi.alive = False
                        gain = pyxel.rndi(1, 4)
                        for i in range(gain):
                            self.sushi_list.append(Sushi(self))
                        break

        if len(self.sushi_list) <= 0:
            self.is_gameover = True

        if not self.player.alive:
            self.is_gameover = True

        for message in self.messages:
            message.update()

        self.messages = [message for message in self.messages if message.alive]


    def draw(self):
        #if self.hit > 0:
        #    pyxel.cls(pyxel.rndi(1,16))
        #else:
        #    pyxel.cls(0)
        pyxel.cls(0)

        if self.is_title:
            self.draw_title()
            return

        if self.is_gameover:
            self.draw_gameover()
            return

        self.draw_score()

        for sushi in self.sushi_list:
            sushi.draw()

        for message in self.messages:
            message.draw()

        self.player.draw()

    def draw_title(self):
        for i in range(1, -1, -1):
            color = 10 if i == 0 else 8
            title_x = WINDOW_WIDTH / 2 - (len(GAME_TITLE) / 2) * 4
            title_y = WINDOW_HEIGHT / 2 - 2

            pyxel.text(title_x, 20 + i, GAME_TITLE, color)
        message = "- Press UP Key -"
        message_x = WINDOW_WIDTH / 2 - (len(message) / 2) * 4

        pyxel.text(message_x, 40 + i, message, 3)

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

    def draw_score(self):
        fscore = f"SCORE:{self.score:04}"
        for i in range(1, -1, -1):
            color = 7 if i == 0 else 0
            pyxel.text(3 + i, 3, fscore, color)

class Player:
    def __init__(self, game, x=None, y=None):
        self.game = (game,)
        self.x = x if x else pyxel.rndi(0, WINDOW_WIDTH)
        self.y = y if y else pyxel.rndi(0, WINDOW_HEIGHT)
        self.speed = 2
        self.size = 8
        self.costume = 1
        self.alive = True
        self.eat_count = 0
        self.enough = False
    
    def eat(self):
        self.eat_count += 1
    
    def refresh(self):
        self.eat_count = 0
        self.enough = False

    def update(self):
        self.costume = self.costume + 1
        if self.costume > 4:
            self.costume = 1
        if self.eat_count > 5:
            self.enough = True

    def speedup(self, flag):
        self.speed = 7 if flag else 2

    def move2(self, x, y):
        self.x = self.x + self.speed * x
        self.y = self.y + self.speed * y

    def up(self):
        self.move2(0, -1)

    def down(self):
        self.move2(0, 1)

    def right(self):
        self.move2(1, 0)

    def left(self):
        self.move2(-1, 0)

    def draw(self):
        if not self.enough:
            pyxel.blt(self.x, self.y, 0, 16, (self.costume % 2) * 8, 8, 8, 0)
        else:
            pyxel.blt(self.x, self.y, 0, 16, 16 + (self.costume % 2) * 8, 8, 8, 0)

class Sushi:
    def __init__(self, game, x=None, y=None):
        self.game = game
        self.x = x if x else pyxel.rndi(0, WINDOW_WIDTH)
        self.y = y if y else pyxel.rndi(0, WINDOW_HEIGHT)
        self.speed = pyxel.rndi(1, 3)
        self.direction_x = pyxel.rndi(1, 3) - 2
        self.direction_y = pyxel.rndi(1, 3) - 2
        self.alive = True
        self.spoiled = False
        self.size = 6
        self.age = 0
        self.spoil = pyxel.rndi(20, 50) * self.speed
        self.life = self.spoil + pyxel.rndi(15, 30)
        self.menu = pyxel.rndi(1, 3)

    def change_direction(self):
        if self.direction_x == -1:
            if self.x <= 3:
                self.direction_x = 1
        if self.direction_x == 1:
            if WINDOW_WIDTH - 6 < self.x:
                self.direction_x = -1
        if self.direction_y == -1:
            if self.y <= 3:
                self.direction_y = 1
        if self.direction_y == 1:
            if WINDOW_HEIGHT - 6 < self.y:
                self.direction_y = -1

    def move(self):
        self.x = self.x + (self.speed * self.direction_x)
        self.y = self.y + (self.speed * self.direction_y)

    def update(self):
        self.age += 1
        if self.age % (5 - self.speed) != 0:
            return
        self.change_direction()
        self.move()
        if self.age > self.spoil:
            self.spoiled = True
            self.direction_x = 0
            self.direction_y = 0

        if self.age > self.life:
            self.alive = False

    def draw(self):
        if self.spoiled:
            pyxel.blt(self.x, self.y, 0, 9, (self.age % 4) * 8, 6, 8, 0)
        else:
            if self.menu == 1:
                pyxel.blt(self.x, self.y, 0, 0, (self.age % 3) * 3, 8, 3, 0)
            elif self.menu == 2:
                pyxel.blt(self.x, self.y, 0, 0, 9 + (self.age % 6) * 3, 8, 3, 0)
            elif self.menu == 3:
                pyxel.blt(self.x, self.y, 0, 0, 27 + (self.age % 2) * 5, 8, 5, 0)

class Message:
    def __init__(self, message, x, y, ttl=10):
        self.message = message
        self.x = y
        self.y = y
        self.ttl = ttl
        self.alive = True
    
    def update(self):
        self.ttl -= 1
        if self.ttl < 0:
            self.alive = False
    
    def draw(self):
        message_x = self.x - (len(self.message) / 2) * 4
        pyxel.text(message_x, self.y, self.message, 3)


SushiGame()
