# from ursina import *

# class ColorMenu(Entity):
#     def __init__(self,EntityToColor,DestoryFunc,**kwargs):
#         super().__init__(parent = camera.ui,**kwargs)
#         self.EntityToColor = EntityToColor
#         self.bg = Button(model = "cube",scale = 99,parent = camera.ui,color = color.black66,highlight_color = color.black66,clicked_color = color.black66,z = -9,on_click = DestoryFunc)
#         self.Menu = Entity(model = "cube",z = -8,render_queue = 10)

#         self.ColorSliderH = Slider(name='h', min=0, max=360, step=1, text='h', dynamic=True, world_parent=self, on_value_changed=self.UpdateColor)


#     def UpdateColor(self):
#         self.EntityToColor.color = color.hsv
# if __name__ == "__main__":
#     app  = Ursina()
#     ColorMenu(None,Func(print_on_screen,'hi',position = (-.1,0)))
#     app.run()

from direct.directbase.DirectStart import *
from panda3d.core import RigidBodyCombiner, NodePath, Vec3
import random

rbc = RigidBodyCombiner("rbc")
rbcnp = NodePath(rbc)
rbcnp.reparentTo(render)

def hi():
    for i in range(2000):
        pos = Vec3(random.uniform(-50, 50),
                random.uniform(-50, 50),
                random.uniform(-50, 50))

        f = loader.loadModel("box.egg")
        f.setPos(pos)
        f.reparentTo(rbcnp)
# def inp():
#     while True:
#         a = input("todo")
#         if a == "1":
#             hi()
# import threading
# threading.Thread(target=inp).start()
hi()
rbc.collect()
base.run()