import pyxel

GAME_TITLE = "DIAGONAL"
WINDOW_WIDTH = 100
WINDOW_HEIGHT = 100
DIAGONAL_UP = 1
DIAGONAL_DN = -1

SIDE_LEFT = -1
SIDE_RIGHT = 1

BLOCK_SIZE = 10
OFFSET_X = 10
OFFSET_Y = 10
TABLE_SIZE = 8


class Block:
    def __init__(self, row, col, diagonal):
        self.row = row
        self.col = col
        self.diagonal = diagonal
        self.x = OFFSET_X + (self.col * BLOCK_SIZE)
        self.y = OFFSET_Y + (self.row * BLOCK_SIZE)
        self.selected = False
        self.right = False
        self.left = False

    def update(self):
        pass

    def draw(self):
        if self.diagonal == DIAGONAL_UP:
            pyxel.line(
                self.x + 1,
                self.y + BLOCK_SIZE - 1,
                self.x + BLOCK_SIZE - 1,
                self.y + 1,
                7,
            )
        else:
            pyxel.line(
                self.x + 1,
                self.y + 1,
                self.x + BLOCK_SIZE - 1,
                self.y + BLOCK_SIZE - 1,
                7,
            )

        if self.selected:
            pyxel.rectb(
                self.x,
                self.y,
                BLOCK_SIZE + 1,
                BLOCK_SIZE + 1,
                2,
            )

        if self.left:
            if self.diagonal == DIAGONAL_UP:
                pyxel.tri(
                    self.x + 1,
                    self.y + 1,
                    self.x + BLOCK_SIZE - 2,
                    self.y + 1,
                    self.x + 1,
                    self.y + BLOCK_SIZE - 2,
                    3,
                )
            else:
                pyxel.tri(
                    self.x + 1,
                    self.y + 2,
                    self.x + 1,
                    self.y + BLOCK_SIZE - 1,
                    self.x + BLOCK_SIZE - 2,
                    self.y + BLOCK_SIZE - 1,
                    3,
                )
        if self.right:
            if self.diagonal == DIAGONAL_UP:
                pyxel.tri(
                    self.x + 2,
                    self.y + BLOCK_SIZE - 1,
                    self.x + BLOCK_SIZE - 1,
                    self.y + BLOCK_SIZE - 1,
                    self.x + BLOCK_SIZE - 1,
                    self.y + 2,
                    3,
                )
            else:
                pyxel.tri(
                    self.x + 2,
                    self.y + 1,
                    self.x + BLOCK_SIZE - 1,
                    self.y + 1,
                    self.x + BLOCK_SIZE - 1,
                    self.y + BLOCK_SIZE - 2,
                    3,
                )

    def select(self, flag):
        self.selected = flag


class Diagonal:
    def __init__(self):
        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT, title=GAME_TITLE, fps=10)
        self.is_title = True
        self.is_gameover = False
        self.score = 0
        self.table = []
        self.cursor_row = 0
        self.cursor_col = 0
        self.turn = 0

    def reset_game(self):
        self.score = 0
        self.table = []
        for rowIdx in range(TABLE_SIZE):
            row = []
            for colIdx in range(TABLE_SIZE):
                b = Block(
                    rowIdx,
                    colIdx,
                    DIAGONAL_UP if pyxel.rndi(1, 2) == 1 else DIAGONAL_DN,
                )
                row.append(b)
            self.table.append(row)
        self.cursor_row = 0
        self.cursor_col = 0

    def update(self):
        if self.is_title or self.is_gameover:
            if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
                self.is_title = False
                self.is_gameover = False
                self.reset_game()
            return
        else:
            if self.turn == 1:
                if pyxel.btn(pyxel.KEY_LEFT):
                    if self.cursor_col == 0:
                        self.cursor_col = TABLE_SIZE - 1
                    else:
                        self.cursor_col -= 1
                if pyxel.btn(pyxel.KEY_RIGHT):
                    if self.cursor_col == TABLE_SIZE - 1:
                        self.cursor_col = 0
                    else:
                        self.cursor_col += 1
                if pyxel.btn(pyxel.KEY_UP):
                    if self.cursor_row == 0:
                        self.cursor_row = TABLE_SIZE - 1
                    else:
                        self.cursor_row -= 1
                if pyxel.btn(pyxel.KEY_DOWN):
                    if self.cursor_row == TABLE_SIZE - 1:
                        self.cursor_row = 0
                    else:
                        self.cursor_row += 1

                if pyxel.btn(pyxel.KEY_A):
                    self.propagete(self.cursor_row, self.cursor_col, SIDE_LEFT)
                if pyxel.btn(pyxel.KEY_B):
                    self.propagete(self.cursor_row, self.cursor_col, SIDE_RIGHT)

        for col in range(TABLE_SIZE):
            for row in range(TABLE_SIZE):
                self.table[row][col].select(
                    (row, col) == (self.cursor_row, self.cursor_col)
                )

    def propagete(self, row, col, side):
        print(row, col, side)

        if side == SIDE_LEFT:
            if self.table[row][col].left:
                return
            else:
                self.table[row][col].left = True

        if side == SIDE_RIGHT:
            if self.table[row][col].right:
                return
            else:
                self.table[row][col].right = True

        if side == SIDE_LEFT and self.table[row][col].left:
            if self.table[row][col].diagonal == DIAGONAL_UP:
                # up-left
                if row > 0:
                    self.propagete(
                        row - 1,
                        col,
                        (
                            SIDE_RIGHT
                            if self.table[row - 1][col].diagonal == DIAGONAL_UP
                            else SIDE_LEFT
                        ),
                    )
                if col > 0:
                    self.propagete(row, col - 1, SIDE_RIGHT)
            else:
                # down-left
                if row < TABLE_SIZE - 1:
                    self.propagete(
                        row + 1,
                        col,
                        (
                            SIDE_LEFT
                            if self.table[row + 1][col].diagonal == DIAGONAL_UP
                            else SIDE_RIGHT
                        ),
                    )
                if col > 0:
                    self.propagete(row, col - 1, SIDE_RIGHT)

        if side == SIDE_RIGHT and self.table[row][col].right:
            if self.table[row][col].diagonal == DIAGONAL_UP:
                # down-right
                if row < TABLE_SIZE - 1:
                    self.propagete(
                        row + 1,
                        col,
                        (
                            SIDE_LEFT
                            if self.table[row + 1][col].diagonal == DIAGONAL_UP
                            else SIDE_RIGHT
                        ),
                    )
                if col < TABLE_SIZE - 1:
                    self.propagete(row, col + 1, SIDE_LEFT)
            else:
                # up-right
                if row > 0:
                    self.propagete(
                        row - 1,
                        col,
                        (
                            SIDE_RIGHT
                            if self.table[row - 1][col].diagonal == DIAGONAL_UP
                            else SIDE_LEFT
                        ),
                    )
                if col < TABLE_SIZE - 1:
                    self.propagete(row, col + 1, SIDE_LEFT)

    def draw(self):
        pyxel.cls(0)

        if self.is_title:
            self.draw_title()
            return

        if self.is_gameover:
            self.draw_gameover()
            return

        self.draw_score()
        #self.draw_debug()
        self.draw_lattice()

        for i in range(TABLE_SIZE):
            for j in range(TABLE_SIZE):
                self.table[i][j].draw()

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

    def draw_debug(self):
        debug = f"row:col={self.cursor_row:02}:{self.cursor_col:02}"
        for i in range(1, -1, -1):
            color = 7 if i == 0 else 0
            pyxel.text(3, WINDOW_HEIGHT - 7 + i, debug, color)

    def draw_lattice(self):
        for i in range(TABLE_SIZE + 1):
            pyxel.line(
                OFFSET_X,
                OFFSET_Y + i * BLOCK_SIZE,
                OFFSET_X + BLOCK_SIZE * TABLE_SIZE,
                OFFSET_Y + i * BLOCK_SIZE,
                7,
            )

            pyxel.line(
                OFFSET_X + i * BLOCK_SIZE,
                OFFSET_Y,
                OFFSET_X + i * BLOCK_SIZE,
                OFFSET_Y + BLOCK_SIZE * TABLE_SIZE,
                7,
            )


diagonal = Diagonal()
pyxel.run(diagonal.update, diagonal.draw)
