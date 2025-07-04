import pyxel
import math

GAME_TITLE = "COYOTE MAN SHOW"
WINDOW_WIDTH = 100
WINDOW_HEIGHT = 100
INITIAL_COUNT = 4

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


def __is_overlapping(a, b):
    x_overlap = a.x <= b.x <= a.x + a.size or a.x < b.x + b.size <= a.x + a.size
    y_overlap = a.y <= b.y <= a.y + a.size or a.y < b.y + b.size <= a.y + a.size

    return x_overlap and y_overlap

def rectangles_overlap(a, b):
    # a, b はそれぞれ4点のタプル（順序は (x1, y1), (x2, y1), (x1, y2), (x2, y2)）
    
    # a の x, y の最小・最大を求める
    ax1 = min(a[0][0], a[2][0])
    ax2 = max(a[1][0], a[3][0])
    ay1 = min(a[0][1], a[1][1])
    ay2 = max(a[2][1], a[3][1])

    # b の x, y の最小・最大を求める
    bx1 = min(b[0][0], b[2][0])
    bx2 = max(b[1][0], b[3][0])
    by1 = min(b[0][1], b[1][1])
    by2 = max(b[2][1], b[3][1])

    # 一方の矩形がもう一方の外側に完全にある場合、重ならない
    if ax2 < bx1 or bx2 < ax1:
        return False
    if ay2 < by1 or by2 < ay1:
        return False

    # 上記で除外されなければ、重なっている
    return True

def circle_overlap(a, b):
    ax, ay, ar = a
    bx, by, br = b

    # 中心点間の距離
    distance = math.hypot(ax - bx, ay - by)

    # 半径の和
    radius_sum = ar + br

    # 距離が半径の和以下なら重なる
    return distance <= radius_sum

def circle(x, y, r, p):
    interval = 360 / p
    d = 0
    while d < 360:
        yield x + math.sin(math.radians(d)) * r, y + math.cos(math.radians(d)) * r
        d += interval

class CoyoteManShowGame:
    def __init__(self):
        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT, title=GAME_TITLE, fps=10)
        pyxel.load("coyote_man_show.pyxres")
        self.init_sound()
        self.is_title = True
        self.is_gameover = False
        self.rakuda = None
        self.chomin_list = []
        self.score = 0
        self.beam_count = 0
        self.hit = False
        self.reset_game()
        self.bgm = None

        pyxel.run(self.update, self.draw)

    def init_sound(self):
        # Set sound effects
        pyxel.sounds[60].set("e2e1e2e1", "p", "7", "s", 5)
        pyxel.sounds[61].set("c1g1c1g1", "p", "7", "s", 5)
        pyxel.sounds[62].set("a3a2c1a1", "p", "7", "s", 5)
        pyxel.sounds[63].set("f3e2a1a1", "n", "7742", "s", 10)

    def reset_game(self):
        self.rakuda = Rakuda(self, WINDOW_WIDTH / 2 - 2, WINDOW_HEIGHT / 2 - 2)
        self.chomin_list = []
        self.score = 0
        self.beam_count = 0

    def update(self):
        if self.hit  > 0:
            self.hit -= 1

        if pyxel.rndi(0, 8) == 0:
            self.chomin_list.append(Chomin(self))

        if self.is_title or self.is_gameover:
            if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
                self.is_title = False
                self.is_gameover = False
                self.bgm = None
                self.reset_game()
            return
        else:
            if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
                self.rakuda.up()
            if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
                self.rakuda.down()
            if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(
                pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT
            ):
                self.rakuda.right()

            if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
                self.rakuda.left()

            if pyxel.btn(pyxel.KEY_B) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_B):
                self.rakuda.beam()


            if pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_A):
                self.rakuda.speedup(True)
            else:
                self.rakuda.speedup(False)

        self.rakuda.update()
        chomin_list = []
        for c in self.chomin_list:
            c.update()
            if c.alive:
                chomin_list.append(c)
        self.chomin_list = chomin_list

        if not self.rakuda.alive:
            self.is_gameover = True
            self.reset_game()

    def draw(self):
        pyxel.cls(0)

        if self.hit > 0:
            pyxel.cls(pyxel.rndi(1,16))
        else:
            pyxel.cls(0)

        if self.is_title:
            self.draw_title()
            return

        if self.is_gameover:
            self.draw_gameover()
            return

        
        if self.bgm is None:
            pyxel.stop()
            self.bgm = 1
            pyxel.playm(self.bgm, loop=True)

        self.draw_score()
        self.draw_beam_count()

        for c in self.chomin_list:
            c.draw()

        self.rakuda.draw()

    def draw_title(self):
        for i in range(1, -1, -1):
            color = 10 if i == 0 else 8
            title_x = WINDOW_WIDTH / 2 - (len(GAME_TITLE) / 2) * 4
            title_y = WINDOW_HEIGHT / 2 - 2

            pyxel.text(title_x, 20 + i, GAME_TITLE, color)
        message = "- Press UP Key -"
        message_x = WINDOW_WIDTH / 2 - (len(message) / 2) * 4

        pyxel.text(message_x, 40 + i, message, 3)
        if self.bgm is None:
            self.bgm = 0
            pyxel.playm(self.bgm, loop=True)

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

    def draw_beam_count(self):
        fscore = f"BEAM:{self.beam_count:02}"
        for i in range(1, -1, -1):
            color = 7 if i == 0 else 0
            pyxel.text(WINDOW_WIDTH - 30 + i, 3, fscore, color)

class Beam:
    def __init__(self, x, y):
        self.r = 0
        self.x = x
        self.y = y
        self.alive = True
    
    def update(self):
        self.r += 7
        if self.r > 40:
            self.alive = False
    
    def draw(self):
        pyxel.play(3, 60, resume=True)
        pyxel.circb(self.x, self.y, self.r, pyxel.rndi(0,8))

class Rakuda:
    def __init__(self, game, x=None, y=None):
        self.game = game
        self.alive = True
        self.speed = 2
        self.direction = 1
        self.x = x if x else pyxel.rndi(0, WINDOW_WIDTH)
        self.y = y if y else pyxel.rndi(0, WINDOW_HEIGHT)
        self.front_legs = 0
        self.rear_legs = 0
        self.stomp_points = []
        self.beams = []

    def speedup(self, flag):
        self.speed = 7 if flag else 2

    def beam(self):
        if self.game.beam_count > 0:
            x = self.x + 24 if self.direction == 1 else self.x
            y = self.y

            self.beams.append(Beam(x, y))
            self.game.beam_count -= 1
        

    def move2(self, x, y):
        self.x = self.x + self.speed * x
        self.y = self.y + self.speed * y

    def up(self):
        self.move2(0, -1)

    def down(self):
        self.move2(0, 1)

    def right(self):
        self.move2(1, 0)
        self.direction = 1

    def left(self):
        self.move2(-1, 0)
        self.direction = -1

    def update(self):
        self.front_legs = pyxel.rndi(0, 2)
        self.rear_legs = pyxel.rndi(0, 2)

        self.stomp_points = []
        self.stomp_points.append(((self.x + 3, self.y + 39), (self.x + 16, self.y + 39), (self.x + 3, self.y + 40), (self.x + 16, self.y + 40)))

        beams = []
        for b in self.beams:
            b.update()
            if b.alive:
                beams.append(b)
        self.beams = beams

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 64, 24 * self.direction * -1, 24, 0)
        offset_y = 88
        offset_leg_front = 0
        offset_leg_rear = 16
        offset_tail = 24

        pyxel.blt(self.x + (0 if self.direction == -1 else 8), self.y + 24, 0, offset_leg_front, offset_y + (16 * self.front_legs), 16 * self.direction * -1, 16, 0)
        pyxel.blt(self.x + (16 if self.direction == -1 else -8), self.y + 24, 0, offset_leg_rear, offset_y + (16 * self.rear_legs), 16 * self.direction * -1, 16, 0)
        pyxel.blt(self.x + (24 if self.direction == -1 else -8), self.y + 16, 0, offset_tail, 80, 8 * self.direction * -1, 8 * (-1 if pyxel.rndi(1, 2) == 1 else 1), 0)

        if self.speed > 5:
            pyxel.play(3, 61, resume=True)

        for b in self.beams:
            b.draw()



class Chomin:
    def __init__(self, game, x=None, y=None, mode=0):
        self.game = game
        self.speed = pyxel.rndi(1, 3)
        self.direction = (-1) ** pyxel.rndi(0, 1)
        self.x = x or (WINDOW_WIDTH if self.direction == -1 else -8)
        self.y = y if y else pyxel.rndi(0, WINDOW_HEIGHT)
        self.mode = mode
        self.age = 0
        self.alive = True
        self.stomped = False
        self.byecount = 0
        self.shocked = False
        self.shockcount = 0
        self.armed = True if self.mode == 0 and pyxel.rndi(0, 4) == 0 else False

    def update(self):
        self.age += 1
        if self.stomped:
            self.byecount -= 1
            if self.byecount < 0:
                if self.mode <= 3:
                    gain = [1,1,1,1,2,2,2,3,3,4,6,12][pyxel.rndi(0,11)]
                    for x, y in circle(self.x, self.y, 20, gain):
                        self.game.chomin_list.append(Chomin(self.game, x, y, self.mode + 1))
                self.alive = False
                self.game.score += 1
                if self.game.score % 5 == 0:
                    self.game.beam_count += 1
        else:
            if self.shocked:
                self.shockcount -= 1
                if self.shockcount <= 0:
                    self.shocked = False
            else:
                if self.mode == 0:
                    self.x += self.direction * self.speed
                    if self.x < -8 or WINDOW_WIDTH < self.x:
                        self.alive = False

        if self.mode > 0:
            if self.age >= pyxel.rndi(15, 30):
                self.alive = False

        hit_area = (
            (self.x + 1, self.y + 1),
            (self.x + 6, self.y + 1),
            (self.x + 6, self.y + 6),
            (self.x + 1, self.y + 6),
        )

        if not self.stomped:
            for stomp_point in self.game.rakuda.stomp_points:
                if rectangles_overlap(hit_area, stomp_point):
                    if self.armed and not self.shocked:
                        self.game.rakuda.alive = False
                        pyxel.play(3, 63, resume=True)
                    else:
                        self.stomped = True
                        self.byecount = 1
                    break

        for beam in self.game.rakuda.beams:
            if circle_overlap((self.x, self.y, 4), (beam.x, beam.y, beam.r)):
                self.shocked = True
                self.shockcount = pyxel.rndi(8, 20)
                break

    def draw(self):
        if self.mode == 0:
            costume = (-1) ** (0 if pyxel.frame_count % 8 <= 3 else 1)
            if self.stomped:
                pyxel.blt(self.x, self.y, 0, 0, 16, 8 * costume, 8, 0)
                pyxel.play(3, 62, resume=True)
            else:
                if self.shocked:
                    pyxel.blt(self.x, self.y, 0, 0, 8, 8 * costume, -8, 0)
                    pyxel.line(self.x + 3, self.y + 7, self.x + 3, self.y + 8, 4)
                else:
                    pyxel.blt(self.x, self.y, 0, 0, 8, 8 * costume, 8, 0)
                    pyxel.line(self.x + 3, self.y - 1, self.x + 3, self.y, 4)
                    if self.armed:
                        idx = self.age % 4
                        katana = [0, 1, 2, 1]
                        if self.direction == 1:
                            pyxel.blt(self.x + 8, self.y + 1, 0, 0, 24 + 8 * katana[idx], -8, 8, 0)
                        else:
                            pyxel.blt(self.x - 8, self.y + 1, 0, 0, 24 + 8 * katana[idx], 8, 8, 0)
        else:
            if self.age < 6:
                pyxel.pset(self.x, self.y, pyxel.rndi(1, 17))
            else:
                if self.stomped:
                    pyxel.blt(self.x, self.y, 0, self.mode * 8, 16, 8, 8, 0)
                    pyxel.play(3, 62, resume=True)
                else:
                    pyxel.blt(self.x, self.y, 0, self.mode * 8, 8, 8, 8, 0)




CoyoteManShowGame()
