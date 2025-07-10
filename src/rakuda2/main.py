import pyxel
from scenes import TitleScene

class Game:
    def __init__(self):
        self.title = "DANCE WITH THE BODY OF DEAD RAKUDA"
        self.window_width = 256
        self.window_height = 256

        self._scenes = {
            "title" : TitleScene(self)
        }

        self._current_scene_name = "title"

        pyxel.init(self.window_width, self.window_height, title=self.title, fps=15)

        

    def get_current_scene(self):
        return self._scenes[self._current_scene_name]
    
    def register_scene(self, scene_name, scene):
        self._scenes[scene_name] = scene

    def notify(self, message):
        pass

    def update(self):
        self.get_current_scene().update()

    def draw(self):
        self.get_current_scene().draw()

    def run(self):
        pyxel.run(self.update, self.draw)

game = Game()
game.run()




