import pyxel

def keypress():
    return [key for key in range(256) if pyxel.btnp(key)]

def keydown():
    return [key for key in range(256) if pyxel.btn(key)]

def keyup():
    return [key for key in range(256) if pyxel.btnr(key)]


