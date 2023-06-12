from typing import Optional
from src.utilities import play_once

import pyxel


class ButtonGroup:
    def __init__(self):
        self.buttons = []
        self.current = 0
        self.focus: Optional[Button] = None

    def update(self):
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.current = (self.current + 1) % len(self.buttons)
            self.set_focus(self.current)
            play_once(3, 1)
        if pyxel.btnp(pyxel.KEY_UP):
            self.current = (self.current - 1) % len(self.buttons)
            self.set_focus(self.current)
            play_once(3, 1)

        self.focus.update()

    def draw(self):
        for button in self.buttons:
            button.draw()

        pyxel.line(self.focus.x - 4, self.focus.y,
                   self.focus.x - 4, self.focus.y + 4,
                   pyxel.COLOR_LIGHT_BLUE)
        pyxel.line(self.focus.x + 4 * len(self.focus.name) + 2, self.focus.y,
                   self.focus.x + 4 * len(self.focus.name) + 2, self.focus.y + 4,
                   pyxel.COLOR_LIGHT_BLUE)

    def get_button_by_tag(self, bid):
        return tuple(filter(lambda x: x.bid == bid, self.buttons))[0]

    def add_button(self, button):
        self.buttons.append(button)

    def set_focus(self, button=0):
        if self.focus:
            self.focus.is_focused = False
        self.focus = self.buttons[button]
        self.focus.is_focused = True
        self.current = button


class Button:
    def __init__(self, x, y, bid, name, callback, *args, **kwargs):
        self.x = x
        self.y = y
        self.bid = bid
        self.name = name
        self.callback = callback
        self.args = args
        self.kwargs = kwargs

        self.is_focused = False
        self.t = 90

    def button_pressed(self):
        self.callback(*self.args, **self.kwargs)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Z) or pyxel.btnp(pyxel.KEY_RETURN):
            play_once(3, 1)
            self.button_pressed()

    def draw(self):
        if self.is_focused:
            self.t += 1
            y = self.y + pyxel.sin(self.t * 10) * 2
        else:
            self.t = 90
            y = self.y

        pyxel.text(self.x, y, self.name, pyxel.COLOR_WHITE)
