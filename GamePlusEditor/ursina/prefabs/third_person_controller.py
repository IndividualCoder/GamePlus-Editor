from GamePlusEditor.ursina import *
from GamePlusEditor.ursina.prefabs.first_person_controller import FirstPersonController


class ThirdPersonController(FirstPersonController):
    def __init__(self, **kwargs):
        super().__init__()
        camera.z = -10


        for key, value in kwargs.items():
            setattr(self, key ,value)


    def input(self, key):
        super().input(key)
        if key == 'scroll down' and camera.z > -20: # zoom out
            camera.z -= time.dt * 50
        if key == 'scroll up' and camera.z < -4: # zoom out
            camera.z += time.dt * 50


if __name__ == '__main__':
    app = Ursina()
    Entity(model='plane', scale=100, collider='box', texture='brick')

    ThirdPersonController(model='cube', y=1, origin_y=-.5, color=color.azure)
    app.run()
