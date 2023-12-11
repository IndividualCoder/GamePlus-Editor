from GamePlusEditor.ursina import Entity, Draggable, Text, Slider, Button, color, Vec3, Quad, invoke
from GamePlusEditor.ursina.prefabs.input_field import InputField


class Space():
    def __init__(self, height=1):
        self.height = height


class WindowPanel(Draggable):
    def __init__(self, title='', content=[], **kwargs):
        self.updateShilderHeight = True
        super().__init__(origin=(-0,.5), scale=(.5, Text.size*2), color=color.black)

        self.content = content
        self.text = title
        self.popup = False
        self._prev_input_field = None
        self._original_scale = self.scale
        self.spacing = .25
        self.height = 1 + self.spacing
        self.CalcAndAddTextLines = True
        self.ToAddHeight = 0
        for key, value in kwargs.items():
            setattr(self, key ,value)

        if self.text_entity:
            self.text_entity.world_scale_y = 1

        self.panel = Entity(parent=self, model='quad', origin=(0,.5), z=.1, color=self.color.tint(.1), collider='box')

        if self.popup:
            self.lock = Vec3(1,1,1)
            # self.bg = Button(parent=self, z=1, scale=(999, 999), color=color.white, highlight_color=color.white, pressed_color=color.white)
##            self.bg.on_click = self.close

        self.layout()


    def layout(self):
        content = self.content
        if not content:
            return
        if isinstance(content, dict):
            content = content.values()

        for c in content:
            # print('........', c)
            # if isinstance(c, Space):
            #     self.height += c.height

            if isinstance(c, Entity):
                c.world_parent = self
                c.position = (0, -self.height, 0)

                if isinstance(c, InputField):
                    if self._prev_input_field:
                        self._prev_input_field.next_field = c
                    self._prev_input_field = c

                if isinstance(c, Text):
                    c.origin = (-.5, .5)
                    c.x = -.48
                    if self.CalcAndAddTextLines:
                        self.height += len(c.lines)
                    else:
                        self.height += self.ToAddHeight

                elif isinstance(c, Button):
                    c.world_parent = self
                    c.scale = (.9, 1)
                    if hasattr(c, 'height'):
                        c.scale_y = self.height
                    c.model = Quad(aspect=c.world_scale_x/c.world_scale_y)
                    self.height += c.scale_y
                    # c.y -= c.scale_y/2

                elif isinstance(c, Slider):
                    c.world_parent = self
                    c.x = -.5 * .9
                    c.scale = (.9*2, 20)
                    # print('-------------', c.scale_y * c.height)
                    if self.updateShilderHeight:
                        print("HIHO")
                        self.height += 1

                # elif hasattr(c, 'scale_y'):
                #     self.height += c.scale_y

                if hasattr(c, 'text_entity') and c.text_entity is not None:
                    c.text_entity.world_scale = (1,1,1)

                self.height += self.spacing
        if self.updateShilderHeight:
            self.panel.scale_y = self.height
        self.panel.model = Quad(aspect=self.panel.world_scale_x/self.panel.world_scale_y, radius=.025)
        self.panel.origin = (0, .5)


    def on_enable(self):
        try:
            if self.popup:
                self.bg.enabled = True
                self.animate_scale(self._original_scale, duration=.1)
        except:
            pass

    def close(self):
        if self.popup:
            self.bg.enabled = False
        self.animate_scale_y(0, duration=.1)
        invoke(setattr, self, 'enabled', False, delay=.2)


if __name__ == '__main__':
    '''
    WindowPanel is an easy way to create UI. It will automatically layout the content.
    '''
    from GamePlusEditor.ursina import Ursina, ButtonGroup
    from GamePlusEditor.ursina import *
    app = Ursina()
    wp = WindowPanel(title='Custom Window',popup = False,content=(Text('Name:'),InputField(name='name_field'),Button(text='Submit', color=color.azure),Slider(),Slider(),ButtonGroup(('test', 'eslk', 'skffk')),ButtonGroup(("Change color","Change scale"))))

    app.run()
