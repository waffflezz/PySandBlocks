import random

import pyxel
from src.particles import Sand
from src.screen import Display
from src.settings import WIDTH, colors, border_y, border_x


def blt_block(x, y, color, skin=0):
    if color == colors[0]:
        pyxel.blt(x, y, 0, 0 + skin * 8, 0, 4, 4)
    elif color == colors[1]:
        pyxel.blt(x, y, 0, 4 + skin * 8, 0, 4, 4)
    elif color == colors[2]:
        pyxel.blt(x, y, 0, 0 + skin * 8, 4, 4, 4)
    elif color == colors[3]:
        pyxel.blt(x, y, 0, 4 + skin * 8, 4, 4, 4)


def get_image_pixel(x, y, color, skin):
    if color == colors[0]:
        x += skin * 8
        return pyxel.image(0).pget(x, y)
    elif color == colors[1]:
        x += 4 + skin * 8
        return pyxel.image(0).pget(x, y)
    elif color == colors[2]:
        x += skin * 8
        y += 4
        return pyxel.image(0).pget(x, y)
    elif color == colors[3]:
        x += 4 + skin * 8
        y += 4
        return pyxel.image(0).pget(x, y)


class Block:
    def __init__(self, x, y, color, display: Display):
        self.x = x
        self.y = y
        self.skin = 0
        self.width = WIDTH
        self.color = color
        self.display = display

    def to_sand(self):
        for y in range(self.y, self.y + self.width):
            for x in range(self.x, self.x + self.width):
                Sand(x, y, self.color,
                     get_image_pixel(x - self.x, y - self.y, self.color,
                                     self.skin), self.display)

    def draw(self):
        blt_block(self.x, self.y, self.color, self.skin)

    def update(self):
        y = self.y + self.width

        if y >= border_y[1]:
            return True

        for x in range(self.x, self.x + self.width):
            if self.display.get_pixel(x, y):
                return True


class Figure:
    def __init__(self, x, y, display):
        self.x = x
        self.y = y
        self.speed = 1
        self.display = display
        self.is_sand = False
        self.is_moveable = True

        self.types = ['J', 'I', 'O', 'L', 'Z', 'T', 'S']
        self.random_types = random.choice(self.types)
        self.random_color = random.choice(colors)

        self.blocks = get_figure(x, y, self.random_color, display,
                                 self.random_types)

        for _ in range(random.randint(1, 4)):
            self.rotate(random.randint(0, 1))

    def check_blocks_border(self):
        all_left_x, all_right_x = [], []
        for block in self.blocks:
            left_x, right_x = block.x, block.x + WIDTH
            if left_x < border_x[0] + 2:
                all_left_x.append(left_x)
            if right_x > border_x[1] - 1:
                all_right_x.append(right_x)

        if all_left_x:
            max_left_x = min(all_left_x)
            offset = abs(border_x[0] + 1 - max_left_x)
            self.update_pos(offset, 0)
            return False
        if all_right_x:
            max_right_x = max(all_right_x)
            offset = abs(max_right_x - border_x[1])
            self.update_pos(-offset, 0)
            return True

    def rotate(self, direction):
        if self.random_types == 'O':
            return
        for block in self.blocks:
            if direction:
                nx = block.y - self.y + self.x
                ny = -block.x + self.x + self.y
            else:
                nx = -block.y + self.y + self.x
                ny = block.x - self.x + self.y
            block.x = nx
            block.y = ny

        self.check_blocks_border()

    def update_pos(self, x, y):
        self.x += x
        self.y += y
        for block in self.blocks:
            block.x += x
            block.y += y

    def update(self):
        if self.is_moveable:
            self.update_pos(0, self.speed)

            self.check_blocks_border()

            if pyxel.btn(pyxel.KEY_LEFT):
                if self.check_blocks_border() is not False:
                    self.update_pos(-2, 0)
            if pyxel.btn(pyxel.KEY_RIGHT):
                if self.check_blocks_border() is not True:
                    self.update_pos(2, 0)

            if pyxel.btnp(pyxel.KEY_X) or pyxel.btnp(pyxel.KEY_UP):
                self.rotate(True)

            if pyxel.btnp(pyxel.KEY_C):
                self.rotate(False)

            if pyxel.btnp(pyxel.KEY_DOWN):
                min_x = min(self.blocks, key=lambda _block: _block.x).x
                max_x = max(self.blocks,
                            key=lambda _block: _block.x + WIDTH).x + WIDTH
                max_y = max(self.blocks,
                            key=lambda _block: _block.y + WIDTH).y + WIDTH
                for y in range(max_y, border_y[1]):
                    for x in range(min_x, max_x):
                        if self.display.display[x][y] or y == border_y[1] - 1:
                            self.update_pos(0, y - max_y - 1)
                            return

        for block in self.blocks:
            if block.update():
                self.is_sand = True
                for block in self.blocks:
                    block.to_sand()
                self.blocks = []
                return

    def draw(self):
        for block in self.blocks:
            block.draw()


def get_figure(x, y, color, display, f_type):
    width = WIDTH
    if f_type == 'J':
        return [Block(x, y, color, display),
                Block(x - width, y, color, display),
                Block(x, y - width, color, display),
                Block(x, y - width * 2, color, display)]
    if f_type == 'I':
        return [Block(x - width * i - width // 2, y, color, display) for i in
                range(-2, 2)]
    if f_type == 'O':
        return [Block(x, y, color, display),
                Block(x - width, y, color, display),
                Block(x - width, y - width, color, display),
                Block(x, y - width, color, display)]
    if f_type == 'L':
        return [Block(x, y - width * i, color, display) for i in range(3)] + [
            Block(x + width, y, color, display)]
    if f_type == 'Z':
        return [Block(x, y, color, display),
                Block(x + width, y, color, display),
                Block(x, y - width, color, display),
                Block(x - width, y - width, color, display)]
    if f_type == 'T':
        return [Block(x - width * i, y, color, display) for i in
                range(-1, 2)] + [Block(x, y - width, color, display)]
    if f_type == 'S':
        return [Block(x, y, color, display),
                Block(x - width, y, color, display),
                Block(x, y - width, color, display),
                Block(x + width, y - width, color, display)]
