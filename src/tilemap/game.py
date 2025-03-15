import pyxel
from collision import push_back

class Game:
    def __init__(self):
        # リソースファイルを読み込む
        pyxel.init(128, 128, title="Tile map")
        pyxel.load("assets/tilemap.pyxres")
        pyxel.tilemaps[2].blt(0, 0, 0, 0, 0, 256, 16)  # 変更前のマップをコピーする

        self.player = None
        self.enemies = []

        self.scenes = {
            "play" : PlayScene(self),
        }
        self.scene_name = None
        self.change_scene("play")

        pyxel.run(self.update, self.draw)

    
    def change_scene(self, name):
        self.scene_name = name
        self.scenes[self.scene_name].start()

    def update(self):
        self.scenes[self.scene_name].update()

    def draw(self):
        self.scenes[self.scene_name].draw()

class Player:
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.direction = 1
        self.jump_counter = 0
        self.dx = 0
        self.dy = 0

    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(
            pyxel.GAMEPAD1_BUTTON_DPAD_LEFT
        ):  # 左キーまたはゲームパッド左ボタンが押されている時
            self.dx = -2
            self.direction = -1

        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(
            pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT
        ):  # 右キーまたはゲームパッド右ボタンが押されている時
            self.dx = 2
            self.direction = 1


        # 下方向に加速する
        if self.jump_counter > 0:  # ジャンプ中
            self.jump_counter -= 1  # ジャンプ時間を減らす
        else:  # ジャンプしていない時
            self.dy = min(self.dy + 1, 4)  # 下方向に加速する

        self.x, self.y = push_back(self.x, self.y, self.dx, self.dy)

        # 横方向の移動を減速する
        self.dx = int(self.dx * 0.8)


    def draw(self):
        # 画像の参照X座標を決める
        u = pyxel.frame_count // 4 % 2 * 8
        # 4フレーム周期で0と8を交互に繰り返す

        # 画像の幅を決める
        w = 8 if self.direction > 0 else -8
        # 移動方向が正の場合は8にしてそのまま描画、負の場合は-8にして左右反転させる

        # 画像を描画する
        pyxel.blt(self.x, self.y, 0, u, 8, w, 8, 0)

   

class PlayScene:
    def __init__(self, game):
        self.game = game

    def start(self):
        pyxel.tilemaps[0].blt(0, 0, 2, 0, 0, 256, 16)
        self.game.player = Player(self.game, 0, 0)
        self.game.screen_x = 0

    def update(self):
        player = self.game.player
        if player:
            player.update()
    
    def draw(self):
        pyxel.bltm(0, 0, 0, self.game.screen_x, 0, 128, 128)
        player = self.game.player
        if player:
            player.draw()
    

