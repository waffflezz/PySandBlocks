class BaseScene:
    def __init__(self, director):
        self.director = director

    def update(self):
        raise NotImplementedError

    def draw(self):
        raise NotImplementedError

    def terminate(self):
        if self.director:
            self.director.scene_stack.remove(self)

    def on_enter(self):
        pass

    def on_exit(self):
        pass


class Director:
    def __init__(self):
        self.scene_stack = []

    def add_scene(self, scene):
        self.scene_stack.append(scene)
        scene.on_enter()

    def remove_scene(self, count=1):
        for _ in range(count):
            self.scene_stack.pop().on_exit()

    def update(self):
        if self.scene_stack:
            self.scene_stack[-1].update()

    def draw(self):
        if self.scene_stack:
            self.scene_stack[-1].draw()
