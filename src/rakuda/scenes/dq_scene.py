import pyxel

class DQScene:
    def __init__(self, game):
        self.game = game
        self.message_template_list = [
            list(reversed(list("おー！らくだよ。しんでしまうとはなさけない"))),
            list(reversed(list("．．．．．．．．．．．．．．．．．．．．．．．．．．．．．．あああ"))),
            list(reversed(list("ここからはなまのらくごをおたのしみください"))),
        ]

        self.message_template_idx = None
        self.message_template = None
        self.message = []
        self.next_message = False

    def reset(self):
        self.age = 0
        self.message_template_idx = 0
        self.message_template = self.message_template_list[self.message_template_idx]
        self.message = []
        self.next_message = False

    def has_message(self):
        return len(self.message) > 0

    def start(self):
        self.reset()
        pyxel.playm(1)

    def stop(self):
        pyxel.stop()

    def update(self):
        self.age += 1

        if self.age < 20:
            return
        
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
                self.game.notify(self, "title")


    def draw(self):
        pyxel.cls(0)
        pyxel.bltm(0, 0, 0, 0, 0, 128, 128, 0)

        if self.has_message():
            pyxel.rectb(4, 80, 120, 40, 0)
            pyxel.rect(5, 81, 118, 38, 7)
            pyxel.rect(6, 82, 116, 36, 0)
            for idx, message in enumerate(self.message):
                pyxel.text(8, 84  + idx * 10, "".join(message), 7, self.game.font)
        
