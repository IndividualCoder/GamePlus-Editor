from GamePlusEditor.ursina import *

class Sky(Entity):

    def __init__(self, **kwargs):
        from GamePlusEditor.ursina.shaders import unlit_shader
        super().__init__(parent=camera, name='sky', model='sky_dome', texture='sky_default', scale=9900, shader=unlit_shader)

        for key, value in kwargs.items():
            setattr(self, key, value)


    def update(self):
        self.world_rotation = Vec3(0,0,0)
        self.scale = camera.clip_plane_far * .95


if __name__  == '__main__':
    app = Ursina()
    Sky(texture='sky_sunset')
    camera.fov = 90
    EditorCamera()
    app.run()
