from ursina import Button, camera, color, Vec3, mouse,Entity


class Cursor(Button):
    def __init__(self, **kwargs):
        super().__init__()
        self.parent = camera.ui
        self.texture = 'cursor'
        self.model = 'quad'
        self.color = color.light_gray
        # self.origin = (-.49, .49)
        self.scale *= .05
        self.render_queue = 1

        for key, value in kwargs.items():
            setattr(self, key, value)


    def update(self):
        self.position = Vec3(mouse.x, mouse.y, -100)




if __name__ == '__main__':
    from ursina import Ursina, Button, scene, Panel, Mesh
    app = Ursina()
    Button('button').fit_to_text()
    camera.orthographic = True
    camera.fov = 100
    cursor =  Cursor(model="cube", scale=.02)
    mouse.visible = False
    app.run()