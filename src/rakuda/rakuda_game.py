import pyxel
import config
from scenes import StandbyScene, TitleScene, PlayScene, DQScene
import math

class Game:

    def __init__(self):
        pyxel.init(config.WINDOW_WIDTH, config.WINDOW_HEIGHT, title=config.TITLE, fps=10)
        pyxel.load("rakuda.pyxres")
        self.title_logo = pyxel.Image(128, 28)
        self.title_logo.load(x=0, y=0, filename="title-logo.png")
        self.font = pyxel.Font("umplus_j10r.bdf")
        self.init_sound()

        self.scenes = {
            "standby": StandbyScene(self),
            "title": TitleScene(self),
            "play": PlayScene(self),
            "dq": DQScene(self)
        }

        self.current_scene = None

    def get_current_scene(self):
        return self.scenes.get(self.current_scene, None)

    def start_scene(self, scene_name):
        stop_list = []
        start = None
        for name, scene in self.scenes.items():
            if name == scene_name:
                start = scene
            else:
                stop_list.append(scene)
        for s in stop_list:
            s.stop()
        start.start()
        self.current_scene = scene_name
        return start

    def notify(self, scene, message, option={}):
        if scene is self.scenes["standby"]:
            if message == "play":
                self.start_scene("play")
            if message == "title":
                self.start_scene("title")
        elif scene is self.scenes["play"]:
            if message == "gameover":
                self.start_scene("dq")
        elif scene is self.scenes["dq"]:
            if message == "standby":
                self.start_scene("standby")
        elif scene is self.scenes["title"]:
            if message == "keypress":
                self.start_scene("standby")
        return

    def init_sound(self):
        # Set sound effects
        pyxel.sounds[60].set("e2e1e2e1", "p", "7", "s", 5)
        pyxel.sounds[61].set("c1g1c1g1", "p", "7", "s", 5)
        pyxel.sounds[62].set("a3a2c1a1", "p", "7", "s", 5)
        pyxel.sounds[63].set("f3e2a1a1", "n", "7742", "s", 10)

    def update(self):
        current_scene = self.get_current_scene()
        if not current_scene:
            current_scene = self.start_scene("standby")

        current_scene.update()

    def draw(self):
        current_scene = self.get_current_scene()
        if current_scene:
            current_scene.draw()

    def start(self):
        pyxel.run(self.update, self.draw)


game = Game()
game.start()
        