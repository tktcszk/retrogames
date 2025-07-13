import pyxel
from scenes import TitleScene, SongScene

class Game:
    def __init__(self):
        self.title = "DANCE WITH THE BODY OF RAKUDA THE ROWDY"
        self.window_width = 256
        self.window_height = 256

        self.subtitles = [
             ("THE WHO ON THE MONTHLY DUTY", "song0")
            ,("OWNER OF THE NAGAYA", "song1")
            ,("GREENGLOCER'S SHOP", "song2")
        ]
        self.subtitle_idx = 0

        pyxel.init(256, 256, title=self.title, fps=15)

        self.scenes = {
            "title": TitleScene(self),
            "song0": SongScene(self, 0),
            "song1": SongScene(self, 1),
            "song2": SongScene(self, 2),

        }
        self.current_scene_name = None

        self.change_scene("title")

        pyxel.load("kankannou.pyxres")
        pyxel.run(self.update, self.draw)

    def get_current_scene(self):
        return self.scenes[self.current_scene_name]
    
    def change_scene(self, scene_name):
        for _, scene in self.scenes.items():
            scene.stop()
        self.current_scene_name = scene_name
        #self.get_current_scene().start()

    def notify(self, sender, message=None):
        if isinstance(sender, TitleScene):
            if message == 'start':
               self.change_scene(self.subtitles[self.subtitle_idx][1])
        if message == "title":
            self.change_scene("title")

        pass

    def get_current_subtitle(self):
        return self.subtitles[self.subtitle_idx][0]

    def update(self):
        self.get_current_scene().update()

    def draw(self):
        self.get_current_scene().draw()


Game()
