import pyxel
from entities import Tobo2, Hero

class DQScene:
    def __init__(self, game):
        self.game = game
        self.message_template_list = [
            list(reversed(list("おー！らくだよ。しんでしまうとはなさけない"))),
            list(reversed(list("．．．．．．．．．．．．．．．．．．．．．．．．．．．．．．あああ"))),
            list(reversed(list("ここからはなまのらくごをおたのしみください"))),
        ]

        self.animation_list = list(reversed([
            (-1,0),(-1,0),(-1,0),(-2,0),(-3,0),(-4,0),(-4,0),(0,-4),(0,4),(0,-4),(0,4),(0,-4),(0,4),(0,4),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0)
            ]))
        
        self.reset()

    def reset(self):
        self.age = 0
        self.message_template_idx = 0
        self.message_template = self.message_template_list[self.message_template_idx]
        self.message = []
        self.next_message = False
        self.entities = []
        self.tobo2 = Tobo2(self, 48, 48)
        self.hero = Hero(self, 64, 64)

        self.entities.append(self.tobo2)
        self.entities.append(self.hero)
        self.is_animation = False
        
        self.dither_count = 0

    def has_message(self):
        return len(self.message) > 0

    def start(self):
        self.reset()
        pyxel.playm(1)

    def stop(self):
        pyxel.stop()
        pyxel.dither(1)

    def update(self):
        self.age += 1

        if self.age < 20:
            return
        
        if self.is_animation:
            self.message = ""
            if len(self.animation_list) > 0:
                move = self.animation_list.pop()
                self.hero.x += move[0]
                self.hero.y += move[1]
            else:
                if self.dither_count < 7:
                    self.dither_count += 1
                else:
                    self.game.notify(self, "standby")

        
        if len(self.message_template) > 0:
            ch = self.message_template.pop()
            if len(self.message) == 0:
                _message = []
                _message.append(ch)
                self.message.append(_message)
            else:
                if len(self.message[len(self.message) - 1]) >= 11 :
                    _message = []
                    _message.append(ch)
                    self.message.append(_message)
                else:
                    self.message[len(self.message) - 1].append(ch)
        else:
            if self.next_message:
                self.message_template_idx += 1
                if self.message_template_idx < len(self.message_template_list):
                    self.message_template = self.message_template_list[self.message_template_idx]
                    self.message = []
                self.next_message = False

        if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
            if self.message_template_idx < len(self.message_template_list):
                self.next_message = True
            else:
                if not self.is_animation:
                    self.is_animation = True

        for entity in self.entities:
            entity.update()


    def draw(self):
        pyxel.cls(0)
        pyxel.bltm(0, 0, 0, 0, 0, 128, 128, 0)
        if self.dither_count > 0:
            pyxel.dither(1 / [1, 2, 4, 8, 16, 32, 64, 128][self.dither_count])

        if self.has_message():
            pyxel.rectb(4, 80, 120, 40, 0)
            pyxel.rect(5, 81, 118, 38, 7)
            pyxel.rect(6, 82, 116, 36, 0)
            for idx, message in enumerate(self.message):
                pyxel.text(8, 84  + idx * 10, "".join(message), 7, self.game.font)

        for entity in self.entities:
            entity.draw()

