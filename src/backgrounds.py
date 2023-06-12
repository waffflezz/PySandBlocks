import random

import pyxel


class Backgrounds:
    def __init__(self):
        self.random_y = [random.randint(2, pyxel.height - 2) for _ in
                         range(random.randint(4, 12))]
        self.lines = [[[0, 0, 0, 0], [0, 0, 0, 0]] for _ in
                      range(len(self.random_y))]

    def update_background_1(self, time):
        if time % 360 == 0:
            self.random_y = [random.randint(2, pyxel.height - 2) for _ in
                             range(random.randint(4, 12))]
            self.lines = [[[0, 0, 0, 0], [0, 0, 0, 0]] for _ in
                          range(len(self.random_y))]

        for i, y in enumerate(self.random_y):
            x = pyxel.sin(time / 2) * pyxel.height
            nx = 0
            self.lines[i][0][0] = x
            self.lines[i][0][1] = y
            self.lines[i][0][2] = nx - 1
            self.lines[i][0][3] = y

            self.lines[i][1][0] = x + pyxel.width
            self.lines[i][1][1] = y
            self.lines[i][1][2] = nx + pyxel.width
            self.lines[i][1][3] = y

    def draw_background_1(self):
        for line in self.lines:
            pyxel.line(line[0][0], line[0][1], line[0][2], line[0][3],
                       pyxel.COLOR_GRAY)
            pyxel.line(line[1][0], line[1][1], line[1][2], line[1][3],
                       pyxel.COLOR_GRAY)
