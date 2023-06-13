import random
from itertools import repeat
import numpy as np

import pyxel

from src.backgrounds import Backgrounds
from src.figures import Figure
from src.liner import line_check
from src.scenes import BaseScene
from src.screen import Display
from src.settings import screen_x, WIDTH
from src.stats import Stats
from src.utilities import play_once, shake, draw_border, draw_mouse
from src.menu_input import ButtonGroup, Button
from src.blocks_3d.engine_3d import Camera, Block


class MainGameScene(BaseScene):
    def __init__(self, director):
        super().__init__(director)
        self.stats = Stats()
        self.display = Display()
        self.backgrounds = Backgrounds()

        self.current_figure = None
        self.game_over = False
        self.camera_offset = repeat((0, 0))

    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            self.director.add_scene(PauseScene(self.director))

        if self.game_over:
            self.director.add_scene(GameOverScene(self.director))
            self.display = Display()
            self.stats = Stats()
            self.current_figure = None
            self.game_over = False

        sand_to_clear = line_check(self.display)
        if sand_to_clear:
            play_once(1, 1)
            self.stats.add_score()
            if self.current_figure:
                self.current_figure.is_moveable = False
            for sand in sand_to_clear:
                self.display.get_pixel(sand[0], sand[1]).line_destroy()
        else:
            if self.current_figure:
                self.current_figure.is_moveable = True

        if not self.current_figure:
            self.current_figure = Figure(screen_x // 2,
                                         WIDTH * 4,
                                         self.display)
            self.current_figure.update()
            if self.current_figure.is_sand:
                self.game_over = True

        if self.current_figure:
            self.current_figure.update()
            if self.current_figure.is_sand:
                pyxel.play(0, 0)
                self.current_figure = None

        if pyxel.btnp(pyxel.KEY_X) or pyxel.btnp(pyxel.KEY_C) or pyxel.btnp(
                pyxel.KEY_UP):
            play_once(3, 1)

        if pyxel.btnp(pyxel.KEY_DOWN):
            play_once(2, 1)
            self.camera_offset = shake()

        pyxel.camera(*next(self.camera_offset))

        if not sand_to_clear:
            self.display.update_sand()

        self.backgrounds.update_background_1(self.stats.time)
        self.stats.update_time()

    def draw(self):
        pyxel.cls(0)

        self.backgrounds.draw_background_1()

        draw_border()

        if self.current_figure:
            self.current_figure.draw()

        self.display.draw_sand()

        self.stats.draw_current_score(2, 12)
        self.stats.draw_time(2, pyxel.height - 26)

        draw_mouse()


class GameOverScene(BaseScene):
    @staticmethod
    def rect_anim():
        for i, x in enumerate(range(pyxel.width // 2, 0, -8)):
            yield x, i * 16
        while True:
            yield 0, pyxel.width

    def __init__(self, director):
        super().__init__(director)
        self.rect = self.rect_anim()

    def update(self):
        if pyxel.btnp(pyxel.KEY_Z):
            self.director.remove_scene()

    def draw(self):
        pyxel.cls(0)
        self.director.scene_stack[-2].draw()
        x, w = next(self.rect)
        pyxel.rect(x, pyxel.height // 2 - 8, w, 16,
                   pyxel.COLOR_YELLOW)
        pyxel.text(pyxel.width // 2 - 20, pyxel.height // 2 - 3, "GAME OVER",
                   pyxel.COLOR_RED)
        pyxel.text(pyxel.width // 2 - 36, pyxel.height // 2 + 10,
                   "Press Z to restart", pyxel.COLOR_WHITE)


class PauseScene(BaseScene):
    def __init__(self, director):
        super().__init__(director)

    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            play_once(3, 1)
            self.director.remove_scene()
        if pyxel.btnp(pyxel.KEY_X):
            play_once(3, 1)
            self.director.remove_scene(3)
            self.director.add_scene(MainMenuScene(self.director))

    def draw(self):
        pyxel.cls(0)
        self.director.scene_stack[-2].draw()
        pyxel.text(pyxel.width // 2 - 9,
                   pyxel.height // 2 + pyxel.sin(
                       pyxel.frame_count * 4) * 4 - 2,
                   "PAUSE", pyxel.COLOR_WHITE)

        pyxel.text(pyxel.width // 2 - 32, pyxel.height - 6,
                   'For exit press X', pyxel.COLOR_WHITE)


class MainMenuScene(BaseScene):
    def __init__(self, director):
        super().__init__(director)
        self.button_group = ButtonGroup()
        self.button_group.add_button(Button(pyxel.width // 2 - 10, 60, 'start',
                                            'Start',
                                            self.director.add_scene,
                                            MainGameScene(self.director)))
        self.button_group.add_button(Button(pyxel.width // 2 - 8, 75, 'skin',
                                            'Skin',
                                            lambda: print('Hello world')))
        self.button_group.add_button(Button(pyxel.width // 2 - 8, 90, 'exit',
                                            'Exit',
                                            pyxel.quit))
        self.button_group.set_focus(0)

        self.camera = Camera(np.array([0., 0., 0.]))
        self.block = None
        self.rx, self.ry, self.rz = None, None, None
        self.random_change_block()

    def random_change_block(self):
        self.block = Block(np.array([0, 10, 100]), 1.5, random.choice(
            ['I', 'J', 'L', 'O', 'S', 'T', 'Z']))
        self.rx, self.ry, self.rz = random.random() / 20, random.random() / 20, random.random() / 20
        self.rx *= 1 if random.random() < 0.5 else -1
        self.ry *= 1 if random.random() < 0.5 else -1
        self.rz *= 1 if random.random() < 0.5 else -1

    def update(self):
        if pyxel.frame_count % 150 == 0:
            self.random_change_block()

        self.block.rotation(self.rx, 'x')
        self.block.rotation(self.ry, 'y')
        self.block.rotation(self.rz, 'z')
        self.button_group.update()

    def draw(self):
        pyxel.cls(0)
        self.block.draw(self.camera)

        pyxel.blt(pyxel.width // 2 - 20, 16, 0, 0, 32, 42, 16)
        pyxel.blt(pyxel.width // 2 - 24, 32, 0, 1, 19, 47, 10)

        self.button_group.draw()

        draw_mouse()
