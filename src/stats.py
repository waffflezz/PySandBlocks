import pyxel


class Stats:
    def __init__(self):
        self.current_score = 0
        self.time = 0

    def add_score(self):
        self.current_score += 2

    def draw_current_score(self, x, y):
        pyxel.text(x, y, f'score:{self.current_score:05}',
                   pyxel.COLOR_WHITE)

    def update_time(self):
        self.time += 1

    def draw_time(self, x, y):
        seconds = self.time // 30
        pyxel.text(x, y, f'time:{seconds // 60:02}:{seconds % 60:02}',
                   pyxel.COLOR_WHITE)
