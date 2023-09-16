from panda3d.core import AntialiasAttrib
from ursina import *

class Game:
  def __init__(self):
      self.item_0 = Entity(parent=scene, name='item_0', enabled=True, eternal=False, position=Vec3(0, 0, 0), rotation=Vec3(0, 0, 0), scale=Vec3(10, 1, 10), model='cube', origin=Vec3(0, 0, 0), shader=None, texture='white_cube', color=color.magenta, collider='mesh', )
      self.item_1 = Entity(parent=scene, name='item_1', enabled=True, eternal=False, position=Vec3(0, 0.44, 0), rotation=Vec3(0, 0, 0), scale=Vec3(1, 1, 1), model='cube', origin=Vec3(0, 0, 0), shader=None, texture='white_cube', color=color.white, collider='mesh', )

if __name__ == '__main__':
    app = Ursina()
    Sky()
    Game()

    def MakeEditorEnvironment(cam,color,size):

        WorldDr = cam.getDisplayRegion(0)
        WorldDr.setDimensions(size)
        base.set_background_color(color[0]/255,color[1]/255,color[2]/255,color[3]/255)
        # print(size)

    MakeEditorEnvironment(application.base.camNode,(5,5,5,1),(0.2, 1, .05, .8)) 
    from ursina.scene import Scene
    from ursina.camera import Camera

    s = Scene()
    s.set_up()
    s.clear()
    # s.entities.append(Button())
    s.fog_density  = .1
    came = Camera()
    came.set_up()
    s.camera = came

    # scene.fog_density  = .1

    render.setAntialias(AntialiasAttrib.MAuto)
    EditorCamera()
    app.run()