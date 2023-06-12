import pyxel
from src.settings import screen_x, screen_y
from src.scenes import Director
from src.game_scenes import MainMenuScene


class App:
    def __init__(self):
        pyxel.init(screen_x, screen_y, title='PySendTetris', quit_key=0)
        pyxel.load('resources.pyxres')

        self.director = Director()
        self.director.add_scene(MainMenuScene(self.director))

        pyxel.run(self.update, self.draw)

    def update(self):
        self.director.update()

    def draw(self):
        self.director.draw()


def main():
    App()


if __name__ == '__main__':
    main()
