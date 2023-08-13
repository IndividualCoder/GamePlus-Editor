from ursina import *
from ursina.shaders import *

from Gizmo import GizmoArrow


class PositionGizmo(Entity):
    def __init__(self, **kwargs):
        super().__init__(parent=scene, enabled=False)
        self.arrow_parent = Entity(parent=self)
        self.lock_axis_helper_parent = Entity(parent=scene,
            model='wireframe_cube',
        )
        self.lock_axis_helper = Entity(parent=self.lock_axis_helper_parent,
            # model=Circle(6, radius=.2), color=color.red, double_sided=True, always_on_top=True, render_queue=1
        ) # this will help us lock the movement to an axis on local space


        self.subgizmos = {
            'xz' : GizmoArrow(parent=self.arrow_parent, gizmo=self, model='cube', collider='plane', scale=.6, scale_y=.05, origin=(-.75,0,-.75), color=lerp(color.magenta, color.cyan, .5), plane_direction=(0,1,0)),
            'x'  : GizmoArrow(parent=self.arrow_parent, gizmo=self, color=axis_colors['x'], lock=(0,1,1)),
            'y'  : GizmoArrow(parent=self.arrow_parent, gizmo=self, rotation=(0,0,-90), color=axis_colors['y'], lock=(1,0,1)),
            'z'  : GizmoArrow(parent=self.arrow_parent, gizmo=self, rotation=(0,-90,0), color=axis_colors['z'], plane_direction=(0,1,0), lock=(1,1,0)),
        }

        for e in self.arrow_parent.children:
            e.highlight_color = color.white
            e.original_scale = e.scale

        self.fake_gizmo = Entity(parent=level_editor, enabled=False)
        self.fake_gizmo.subgizmos = dict()
        for key, value in self.subgizmos.items():
            self.fake_gizmo.subgizmos[key] = duplicate(self.subgizmos[key], parent=self.fake_gizmo, collider=None, ignore=True)


    def input(self, key):   # this will execute before GizmoArrow drag()
        if key == 'left mouse down' and mouse.hovered_entity in self.subgizmos.values():
            self.drag()

        if key == 'left mouse up' and level_editor.local_global_menu.value == 'local':
            self.drop()


    def drag(self, show_gizmo_while_dragging=True):
        for i, axis in enumerate('xyz'):
            self.subgizmos[axis].plane_direction = self.up

            self.subgizmos[axis].lock = [0,0,0]
            if level_editor.local_global_menu.value == 'global':
                self.subgizmos[axis].lock = [1,1,1]
                self.subgizmos[axis].lock[i] = 0

            if axis == 'y':
                self.subgizmos[axis].plane_direction = camera.back


        self.subgizmos['xz'].plane_direction = self.up
        [setattr(e, 'visible_self', show_gizmo_while_dragging) for e in self.subgizmos.values()]


        # use fake gizmo technique to lock movement to local axis. if in global mode, skip this and use the old simpler way.
        if level_editor.local_global_menu.value == 'local':
            self.lock_axis_helper_parent.world_transform = self.world_transform
            self.lock_axis_helper.position = (0,0,0)
            self.fake_gizmo.world_transform = self.world_transform

            self.fake_gizmo.enabled = True
            self.visible = False
            [setattr(e, 'visible_self', show_gizmo_while_dragging) for e in self.fake_gizmo.subgizmos.values()]
            [setattr(e, 'visible_self', False) for e in self.subgizmos.values()]


    def drop(self):
        self.fake_gizmo.enabled = False
        self.visible = True
        [setattr(e, 'visible_self', False) for e in self.fake_gizmo.subgizmos.values()]
        [setattr(e, 'visible_self', True) for e in self.subgizmos.values()]
        [setattr(e, 'scale', e.original_scale) for e in self.subgizmos.values()]


    def update(self):
        # self.world_scale = distance(self.world_position, camera.world_position) * camera.fov * .0005

        for i, axis in enumerate('xyz'):
            if self.subgizmos[axis].dragging:
                setattr(self.lock_axis_helper, axis, self.subgizmos[axis].get_position(relative_to=self.lock_axis_helper_parent)[i])
                self.fake_gizmo.world_position = self.lock_axis_helper.world_position

        if self.subgizmos['xz'].dragging:
            self.fake_gizmo.world_position = self.subgizmos['xz'].world_position
