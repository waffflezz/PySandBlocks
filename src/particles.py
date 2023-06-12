import pyxel
from src.settings import border_x, border_y


class Particle:
    def __init__(self, x, y, color, mutable_color, display):
        self.x = x
        self.y = y
        self.color = color
        self.mutable_color = mutable_color
        self.display = display

        self.delay = 30

        self.display.set_pixel(x, y, self)

    def draw(self):
        pyxel.pset(self.x, self.y, self.mutable_color)

    def move_to(self, x, y):
        self.display.set_pixel(self.x, self.y, None)
        self.x = x
        self.y = y
        self.display.set_pixel(self.x, self.y, self)

    def line_destroy(self):
        if self.delay > 0:
            self.delay -= 1
            self.mutable_color = pyxel.frame_count % 16
            return
        self.display.set_pixel(self.x, self.y, None)


class Sand(Particle):
    def __init__(self, x, y, color, mutable_color, display):
        super().__init__(x, y, color, mutable_color, display)

    def update(self):
        bottom_pixel = self.display.get_pixel(self.x, self.y + 1)
        left_bottom_pixel = self.display.get_pixel(self.x - 1, self.y + 1)
        right_bottom_pixel = self.display.get_pixel(self.x + 1, self.y + 1)

        if bottom_pixel and left_bottom_pixel and right_bottom_pixel:
            return

        if self.y == border_y[1] - 1:
            return

        if self.x <= border_x[0] + 1:
            if bottom_pixel and not right_bottom_pixel:
                self.move_to(self.x + 1, self.y + 1)
                return

        if self.x >= border_x[1] - 1:
            if bottom_pixel and not left_bottom_pixel:
                self.move_to(self.x - 1, self.y + 1)
                return

        if self.x <= border_x[0] + 1 or self.x >= border_x[1] - 1:
            if bottom_pixel:
                return

        if bottom_pixel is None:
            self.move_to(self.x, self.y + 1)
            return

        if isinstance(bottom_pixel, Particle):
            if isinstance(left_bottom_pixel, Particle) and isinstance(
                    right_bottom_pixel, Particle):
                return
            elif left_bottom_pixel is None:
                self.move_to(self.x - 1, self.y + 1)
                return
            elif right_bottom_pixel is None:
                self.move_to(self.x + 1, self.y + 1)
                return
