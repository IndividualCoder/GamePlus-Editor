# from ursina import *

# class NewDraggable(Button):
#     def __init__(self, ReturnValue, **kwargs):
#         super().__init__(**kwargs)

#         self.ReturnValue: function = ReturnValue
#         self.Dragging = False
#         self.StartPos = mouse.position
#         self.LastPos = self.StartPos

#     def input(self,key):
#         if self.hovered and key == 'left mouse down':
#             # self.StartDragging()
#             if hasattr(self,"drag"):
#                 self.drag()
#             self.StartPos = mouse.position
#             self.Dragging = True

#         if self.Dragging and key == 'left mouse up':
#             # self.StopDragging()
#             if hasattr(self,"drop"):
#                 self.drop()
#             self.Dragging = False

#     def update(self):
#         if not self.Dragging:
#             return
#         # if not self.hovered:
#         #     return

#         self.ReturnValue(Vec3(mouse.position.x-self.StartPos.x))
#         self.LastPos = mouse.position
#         # self.StartPos = mouse.

# if __name__ == "__main__":
#     app = Ursina()
#     def ret(val):
#         print(val)
#     a = NewDraggable(ret,parent = scene)
#     EditorCamera()

#     app.run()

from GamePlusEditor.ursina import *

class NewDraggable(Button):

    _z_plane = Entity(name='_z_plane', scale=(9999,9999), enabled=False, eternal=True)

    def __init__(self,RetVal,Entity, **kwargs):
        super().__init__(**kwargs)
        self.require_key = None
        self.dragging = False
        self.delta_drag = 0
        self.start_pos = self.world_position
        self.start_offset = (0,0,0)
        self.step = (0,0,0)
        self.plane_direction = (0,0,1)
        self.lock = Vec3(0,0,0)     # set to 1 to lock movement on any of x, y and z axes
        self.min_x, self.min_y, self.min_z = -inf, -inf, -inf
        self.max_x, self.max_y, self.max_z = inf, inf, inf
        self.RetVal = RetVal
        self.Enti = Entity
        self.sensitivity = 10
        self.axis = Vec3(1,0,0)

        if not Draggable._z_plane.model: # set these after game start so it can load the model
            Draggable._z_plane.model = 'quad'
            Draggable._z_plane.collider = Mesh(vertices=((-0.5, -0.5, 0.0), (0.5, -0.5, 0.0), (0.5, 0.5, 0.0), (-0.5, 0.5, 0.0)), triangles=((0,1,2,3),), mode='triangle')
            Draggable._z_plane.color = color.clear


        for key, value in kwargs.items():
            if key == 'collider' and value == 'sphere' and self.has_ancestor(camera.ui):
                print('error: sphere colliders are not supported on Draggables in ui space.')

            if key == 'text' or key in self.attributes:
                continue

            setattr(self, key, value)


    def input(self, key):
        if self.hovered and key == 'left mouse down':
            if self.require_key == None or held_keys[self.require_key]:
                self.start_dragging()

        if self.dragging and key == 'left mouse up':
            self.stop_dragging()


    def start_dragging(self):
        point = Vec3(0,0,0)
        if mouse.world_point:
            point = mouse.world_point

        Draggable._z_plane.world_position = point
        # Draggable._z_plane.world_position = self.world_position
        Draggable._z_plane.look_at(Draggable._z_plane.position - Vec3(*self.plane_direction))
        if self.has_ancestor(camera.ui):
            Draggable._z_plane.world_parent = camera.ui
        else:
            Draggable._z_plane.world_parent = scene

        self.start_offset = point - self.world_position
        self.dragging = True
        self.start_pos = self.world_position
        self.collision = False
        Draggable._z_plane.enabled = True
        mouse._original_traverse_target = mouse.traverse_target
        mouse.traverse_target = Draggable._z_plane
        if hasattr(self, 'drag'):
            self.drag()


    def stop_dragging(self):
        self.dragging = False
        self.delta_drag = self.world_position - self.start_pos
        Draggable._z_plane.enabled = False
        self.collision = True
        if hasattr(mouse, '_original_traverse_target'):
            mouse.traverse_target = mouse._original_traverse_target
        else:
            mouse.traverse_target = scene

        if hasattr(self, 'drop'):
            self.drop()

    # def drag(self):
    #     print('start drag test')
    #
    # def drop(self):
    #     print('drop test')

    def update(self):
        if self.dragging:
            global hor_step,ver_step,dep_step
            if mouse.world_point:
                if not self.lock[0]:
                    self.hehe_world_x = mouse.world_point[0] - self.start_offset[0]
                elif self.lock[0]:
                    self.hehe_world_x = 1
                if not self.lock[1]:
                    self.hehe_world_y = mouse.world_point[1] - self.start_offset[1]
                elif self.lock[1]:
                    self.hehe_world_y = 1
                if not self.lock[2]:
                    self.hehe_world_z = mouse.world_point[2] - self.start_offset[2]
                elif self.lock[2]:
                    self.hehe_world_z = 1

            hor_step,ver_step,dep_step = 1,1,1

            if self.step[0] > 0:
                hor_step = 1/self.step[0]
                # self.x = round(self.x * hor_step) /hor_step
            if self.step[1] > 0:
                ver_step = 1/self.step[1]
                # self.y = round(self.y * ver_step) /ver_step
            if self.step[2] > 0:
                dep_step = 1/self.step[2]
                # self.z = round(self.z * dep_step) /dep_step

            ToReturn = Vec3(sum(mouse.velocity), sum(mouse.velocity), sum(mouse.velocity)) * self.sensitivity * time.dt * self.axis
            # if self.step[0] == 0:
            self.RetVal(ToReturn, self.Num)
            # else:
            #     if  self.step[0] % ToReturn[self.Num] == 0:
            #         self.RetVal(ToReturn, self.Num)


    @property
    def step(self):
        return self._step

    @step.setter
    def step(self, value):
        if isinstance(value, (int, float, complex)):
            value = (value, value, value)

        self._step = value



if __name__ == '__main__':
    app = Ursina()

    Entity(model='plane', scale=8, texture='white_cube', texture_scale=(8,8))
    draggable_button = Draggable(scale=.1, text='drag me', position=(-.5, 0))
    world_space_draggable = Draggable(parent=scene, model='cube', color=color.azure, a= (0,1,0), lock=(1,0,0))

    EditorCamera(rotation=(0,0,0))
    world_space_draggable.drop = Func(print, 'dropped cube')

    app.run()