'''
Inspired from ursina's editor
'''

from ursina import *
from ursina.shaders import *

class GizmoArrow(Draggable):
    '''Not done yet ;)'''
    def __init__(self,world_parent = scene, model='arrow', collider='box', **kwargs):
        super().__init__(model=model, origin_x=-.55, always_on_top=True, render_queue=1, is_gizmo=True, shader=unlit_shader, **kwargs)
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.three_d_parent = world_parent
        # self.record_undo = True     # this can be set to False when moving this though code for example, and you don't want it to record undo.
        self.original_rotation = self.rotation


    def drag(self):
        self.world_parent = self.three_d_parent
        self.gizmo.world_parent = self
        for e in level_editor.selection:
            e.original_parent = e.parent

            if level_editor.local_global_menu.value == 'global':
                e.world_parent = self
            else:
                e.world_parent = self.gizmo.fake_gizmo

            e.always_on_top = False
            e._original_world_transform = e.world_transform

    def drop(self):
        self.gizmo.world_parent = level_editor

        for e in level_editor.selection:
            e.world_parent = e.original_parent

        if not level_editor.selection:
            return

        changed = ( # don't record undo if transform didn't change
            distance(level_editor.selection[0].world_transform[0], level_editor.selection[0]._original_world_transform[0]) > .0001 or
            distance(level_editor.selection[0].world_transform[1], level_editor.selection[0]._original_world_transform[1]) > .0001 or
            distance(level_editor.selection[0].world_transform[2], level_editor.selection[0]._original_world_transform[2]) > .0001
            )

        if self.record_undo and changed:
            changes = []
            for e in level_editor.selection:
                changes.append([level_editor.entities.index(e), 'world_transform', e._original_world_transform, e.world_transform])

            level_editor.current_scene.undo.record_undo(changes)

        self.parent = self.gizmo.arrow_parent
        self.position = (0,0,0)
        self.rotation = self.original_rotation
        level_editor.render_selection()

    def input(self, key):
        super().input(key)
        if key == 'control':
            self.step = (.1,.1,.1)
        elif key == 'control up':
            self.step = (0,0,0)
