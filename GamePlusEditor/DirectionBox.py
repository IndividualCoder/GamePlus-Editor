from GamePlusEditor.ursina import Entity,Text,color,mouse,Vec3,held_keys

# inspired from ursina.editor.editor import PointOfViewSelector

class PointOfViewSelector(Entity):
    '''As told above, inspired from ursina's gui editor'''
    def __init__(self,parent,pos,editor_camera,camera, **kwargs):
        self.camera = camera
        super().__init__(parent=parent, model='cube', collider='box', texture='white_cube', scale=.05, position=pos)
        self.front_text = Text(parent=self, text='Front', z=-.5, scale=10, origin=(0,0), color=color.azure)
        self.back_text = Text(parent=self, text='Back', z=.5, scale=10, origin=(0,0), color=color.green,double_sided = False,rotation = (180,0,180))
        self.left_text = Text(parent=self, text='Left', z=0,x = .5, scale=10, origin=(0,0), color=color.yellow,double_sided = False,rotation = (0,-90,0))
        self.right_text = Text(parent=self, text='Right', z=0,x = -.5, scale=10, origin=(0,0), color=color.orange,double_sided = False,rotation = (0,90,0))
        self.top_text = Text(parent=self, text='Top', z = 0,y = .5, scale=10, origin=(0,0), color=color.dark_gray,double_sided = False,rotation = (90,0,0))
        self.bottom_text = Text(parent=self, text='Bottom', z=0,y = -.5, scale=10, origin=(0,0), color=color.pink,double_sided = False,rotation = (-90,0,0))

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
        # print(self.editor_camera.rotation)

    def input(self, key):
        if held_keys['shift']:
            if key == '1':   self.editor_camera.animate_rotation((0,0,0)) # front
            elif key == '2':   self.editor_camera.animate_rotation((0,180,0)) # front
            elif key == '3': self.editor_camera.animate_rotation((0,-90,0)) # left
            elif key == '4': self.editor_camera.animate_rotation((0,90,0)) # right
            elif key == '5': self.editor_camera.animate_rotation((90,0,0)) # top
            elif key == '6': self.editor_camera.animate_rotation((-90,0,0)) # bottom

            # elif key == '7': self.editor_camera.animate_rotation((90,0,0)) # top
            # elif key == '5': self.camera.orthographic = not self.camera.orthographic


if __name__ == "__main__":
    from GamePlusEditor.ursina import *
    DirectionEntity = PointOfViewSelector(camera.ui,(0,0,0),EditorCamera(),camera,enabled = True,z = -30,scale = 10)
