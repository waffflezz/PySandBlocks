import pyxel

from src.settings import border_x, border_y


class Display:
    def __init__(self):
        self.display = []
        for i in range(pyxel.width):
            self.display.append([])
            for j in range(pyxel.height):
                self.display[i].append(None)

    @staticmethod
    def check_coords(x, y):
        if x <= border_x[0] or x >= border_x[1]:
            return None
        if y <= border_y[0] or y >= border_y[1]:
            return None
        return True

    def get_pixel(self, x, y):
        if self.check_coords(x, y):
            return self.display[x][y]

    def set_pixel(self, x, y, value):
        if self.check_coords(x, y):
            self.display[x][y] = value

    def draw_sand(self):
        for row in self.display:
            for sand in row:
                if sand:
                    sand.draw()

    def update_sand(self):
        for j in range(pyxel.height - 1, -1, -1):
            for i in range(pyxel.width):
                sand = self.display[i][j]
                if sand:
                    sand.update()
