# inspired from pokepetter's editor's PointOfViewSelect
from ursina import Entity,Text,color,mouse,Vec3,held_keys

# inspired from ursina.editor.editor import PointOfViewSelector
class PointOfViewSelector(Entity):
    def __init__(self,parent,pos,editor_camera,camera, **kwargs):
        self.camera = camera
        super().__init__(parent=parent, model='cube', collider='box', texture='white_cube', scale=.05, position=pos)
        self.front_text = Text(parent=self, text='Front', z=-.5, scale=10, origin=(0,0), color=color.azure)
        self.back_text = Text(parent=self, text='Back', z=.5, scale=10, origin=(0,0), color=color.azure,double_sided = False,rotation = (180,0,180))
        self.editor_camera = editor_camera
        for key, value in kwargs.items():
            setattr(self, key, value)

    def on_click(self):
        if mouse.normal == Vec3(0,0,-1):   self.editor_camera.animate_rotation((0,0,0)) # front
        elif mouse.normal == Vec3(0,0,1):  self.editor_camera.animate_rotation((0,180,0)) # back
        elif mouse.normal == Vec3(1,0,0):  self.editor_camera.animate_rotation((0,90,0)) # right
        elif mouse.normal == Vec3(-1,0,0): self.editor_camera.animate_rotation((0,-90,0)) # right
        elif mouse.normal == Vec3(0,1,0):  self.editor_camera.animate_rotation((90,0,0)) # top
        elif mouse.normal == Vec3(0,-1,0): self.editor_camera.animate_rotation((-90,0,0)) # top


    def update(self):
        self.rotation = -self.editor_camera.rotation

    def input(self, key):
        if held_keys['shift']:
            if key == '1':   self.editor_camera.animate_rotation((0,0,0)) # front
            elif key == '3': self.editor_camera.animate_rotation((0,90,0)) # right
            elif key == '7': self.editor_camera.animate_rotation((90,0,0)) # top
            # elif key == '7': self.editor_camera.animate_rotation((90,0,0)) # top
            # elif key == '5': self.camera.orthographic = not self.camera.orthographic
