import pyxel

from src.settings import border_x, border_y, border_color


def draw_border():
    pyxel.line(border_x[0], border_y[0], border_x[0], border_y[1],
               border_color)
    pyxel.line(border_x[0], border_y[0], border_x[1], border_y[0],
               border_color)
    pyxel.line(border_x[0], border_y[1], border_x[1], border_y[1],
               border_color)
    pyxel.line(border_x[1], border_y[0], border_x[1], border_y[1],
               border_color)
    pyxel.rect(border_x[0] + 1, border_y[0] + 1,
               border_x[1] - border_x[0] - 1,
               border_y[1] - border_y[0] - 1, pyxel.COLOR_BLACK)


def draw_mouse():
    mx, my = pyxel.mouse_x, pyxel.mouse_y
    pyxel.line(mx, my, mx + 2, my, pyxel.COLOR_WHITE)
    pyxel.line(mx, my, mx, my + 2, pyxel.COLOR_WHITE)
    pyxel.line(mx, my, mx + 3, my + 3, pyxel.COLOR_WHITE)


def play_once(sound, channel):
    playing_sound = pyxel.play_pos(channel)
    if playing_sound:
        if sound == playing_sound[0]:
            return
    else:
        pyxel.play(channel, sound)


def shake():
    for y in range(0, 4, 2):
        yield 0, -y
    for y in range(4, 0, -2):
        yield 0, -y
    while True:
        yield 0, 0
