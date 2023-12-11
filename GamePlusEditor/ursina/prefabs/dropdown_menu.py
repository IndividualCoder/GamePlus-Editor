from GamePlusEditor.ursina import *


class DropdownMenuButton(Button):
    def __init__(self, text='', **kwargs):
        super().__init__(
            scale=(.25,.025),
            origin=(-.5,.5),
            pressed_scale=1,
            text=text,
            **kwargs
            )

        if self.text_entity:
            self.text_entity.x = .05
            self.text_entity.origin = (-.5, 0)
            self.text_entity.scale *= .8

class SimpleDropdownMenu(DropdownMenuButton):

    def __init__(self, text='', buttons=list(),click_to_open = False, **kwargs):
        super().__init__(text=text)
        self.is_open = False
        self.position = window.top_left
        self.buttons = buttons

        self.UnhoverToExit = click_to_open
        for i, b in enumerate(self.buttons):
            b.world_parent = self
            b.original_scale = b.scale
            b.x = 0
            b.y = -i-1 *.98
            b.enabled = False

            if isinstance(b, DropdownMenu):
                for e in b.buttons:
                    e.x = 1
                    e.y += 1

        self.arrow_symbol = Text(text = ">",world_parent=self, origin=(0,0), position=(.95, -.5),color = color.white)
        # self.arrow_symbol.scale_override
        for key, value in kwargs.items():
            setattr(self, key, value)


    def open(self):
        for i, b in enumerate(self.buttons):
            invoke(setattr, self.buttons[i], 'enabled', True, delay=(i*.02))
        # self.arrow_symbol.animate_rotation_z(90,.4)

        # self.arrow_symbol.rotate(Vec3(0,0,90))
        # self.arrow_symbol.animate_scale(Vec3(40,4,1),.4)
        # self.arrow_symbol.scale = (40,4,1)
        # self.arrow_symbol.rotation_z = 90
        self.is_open = True
        # self.arrow_symbol.look_at(self.arrow_symbol.position + Vec3(0, 0, 1))
        print(self.arrow_symbol.scale)

    def close(self):
        for i, b in enumerate(reversed(self.buttons)):
            b.disable()
        self.is_open =False
        self.arrow_symbol.rotation_z = 0
        self.arrow_symbol.animate_rotation_z(0,.4)
        # self.arrow_symbol.animate_scale(Vec3(4,40,1),.4)
        # self.arrow_symbol.scale = (4,40,1)
    def input(self, key):
        if key == 'left mouse down' and mouse.hovered_entity and mouse.hovered_entity.has_ancestor(self):
            if type(mouse.hovered_entity) != DropdownMenu:
                self.close()
        if key == "escape":
            self.close()

    def on_click(self):
        if self.is_open:
            self.close()
        else:
            self.open()


class DropdownMenu(DropdownMenuButton):

    def __init__(self, text='', buttons=list(),click_to_open = False, **kwargs):
        super().__init__(text=text)
        self.position = window.top_left
        self.buttons = buttons

        self.UnhoverToExit = click_to_open
        for i, b in enumerate(self.buttons):
            b.world_parent = self
            b.original_scale = b.scale
            b.x = 0
            b.y = -i-1 *.98
            b.enabled = False

            if isinstance(b, DropdownMenu):
                for e in b.buttons:
                    e.x = 1
                    e.y += 1

        self.arrow_symbol = Text(world_parent=self, text='>', origin=(.5,.5), position=(.95, 0), color=color.gray)
        for key, value in kwargs.items():
            setattr(self, key, value)


    def open(self):
        for i, b in enumerate(self.buttons):
            invoke(setattr, self.buttons[i], 'enabled', True, delay=(i*.02))

    def close(self):
        for i, b in enumerate(reversed(self.buttons)):
            b.disable()


    def on_mouse_enter(self):
        super().on_mouse_enter()
        self.open()

    def input(self, key):
        if key == 'left mouse down' and mouse.hovered_entity and mouse.hovered_entity.has_ancestor(self) and not self.UnhoverToExit:
            self.close()

    def update(self):
        if self.hovered or mouse.hovered_entity and mouse.hovered_entity.has_ancestor(self):
            return

        self.close()


if __name__ == '__main__':
    from GamePlusEditor.ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton

    app = Ursina()
    # DropdownMenu(text='File')
    DropdownMenu('File', buttons=(
        DropdownMenuButton('New'),
        DropdownMenuButton('Open'),
        DropdownMenu('Reopen Project', buttons=(
            DropdownMenuButton('Project 1'),
            DropdownMenuButton('Project 2'),
            )),
        DropdownMenuButton('Save',on_click = Func(print,"Saved")),
        DropdownMenu('Options', buttons=(
            DropdownMenuButton('Option a'),
            DropdownMenuButton('Option b'),
            )),
        DropdownMenuButton('Exit'),
        ),click_to_open=True)

    app.run()
