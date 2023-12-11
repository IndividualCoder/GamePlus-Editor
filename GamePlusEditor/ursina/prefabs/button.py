from GamePlusEditor.ursina import Entity, Text, camera, color, mouse, BoxCollider, Sequence, Func, Vec2, Vec3, scene,held_keys
from GamePlusEditor.ursina.models.procedural.quad import Quad
import textwrap
from GamePlusEditor.ursina import color as colour


# made tool tip work as expected
class Button(Entity):

    color = color.black66
    default_model = None  # will default to rounded Quad
    default_values = {
        'parent':camera.ui,
        'name':'button', 'enabled':True, 'eternal':False, 'position':Vec3(0,0,0), 'rotation':Vec3(0,0,0), 'scale':Vec3(.3,.3,.3), 'model':default_model, 'origin':Vec3(0,0,0),
        'shader':None, 'texture':None, 'color':color}

    def __init__(self, text='', radius=.1, ToSubtract=0, Key=None,partKey = "",on_key_press = None,on_hover = None,on_unhover = None,hover_highlight = False,hover_highlight_color = colour.white,hover_highlight_size = .2,hover_highlight_button = False, **kwargs):
        super().__init__()
        self.hover_highlight_color = hover_highlight_color
        self.hover_highlight = hover_highlight
        self.hover_highlight_button = hover_highlight_button
        self.parent  = camera.ui

        # self.render_queue
        self.disabled = False
        self._on_click = None
        self.on_hover = on_hover
        self.on_unhover = on_unhover
        if on_key_press is None:
            self.on_key_press = self.on_click  # Custom on_key_press attribute
        else:
            self.on_key_press = on_key_press
        self.ToSubtract = ToSubtract #To small text
        if "tool_tip" in kwargs:
            self.tool_tip = kwargs["tool_tip"]
        else:
            self.tool_tip = None
        self.partKey = partKey
        self.Key = Key  # Custom Key attribute
        for key, value in kwargs.items():
            if key in (
                'scale', 'scale_x', 'scale_y', 'scale_z',
                'world_scale', 'world_scale_x', 'world_scale_y', 'world_scale_z',
            ):
                setattr(self, key, value)

        if self.hover_highlight:
            self.highlight_button = Button(parent = self,enabled = True,radius=radius,color = color.clear,scale = (self.scale_x+hover_highlight_size,self.scale_y+hover_highlight_size),hover_highlight_button = True,z = 0)



        if Button.default_model is None:
            if 'model' not in kwargs and self.scale[0] != 0 and self.scale[1] != 0:
                self.model = Quad(aspect=self.scale[0] / self.scale[1], radius=radius)
        else:
            self.model = Button.default_model
        self.color = Button.color

        self.text_entity = None
        if text:
            self.text = text

        if 'color' in kwargs:
            setattr(self, 'color', kwargs['color'])
        self.highlight_color = self.color.tint(.2)
        self.pressed_color = self.color.tint(-.2)
        self.highlight_scale = 1  # multiplier
        self.pressed_scale = 1  # multiplier
        self.collider = 'box'

        for key, value in kwargs.items():
            setattr(self, key, value)

        self.original_scale = self.scale
        if self.text_entity is not None:
            self.text_entity.world_scale = 1

        self.icon = None

    @property
    def text(self):
        if self.text_entity:
            return self.text_entity.text

    @text.setter
    def text(self, value):
        if isinstance(value, str):
            if not self.text_entity:
                self.text_entity = Text(
                    parent=self,
                    size=Text.size * 20 - self.ToSubtract,
                    position=(-self.origin[0], -self.origin[1], -.1),
                    origin=(0, 0),
                    add_to_scene_entities=False,
                )

            self.text_entity.text = value
            self.text_entity.world_scale = (1, 1, 1)

    @property
    def text_origin(self):
        if not self.text_entity:
            return (0, 0)

        return self.text_entity.origin

    @text_origin.setter
    def text_origin(self, value):
        if not self.text_entity:
            return

        self.text_entity.world_parent = self.model
        self.text_entity.position = value
        self.text_entity.origin = value
        self.text_entity.world_parent = self

    @property
    def text_color(self):
        return self.text_entity.color

    @text_color.setter
    def text_color(self, value):
        self.text_entity.color = value

    @property
    def icon(self):
        return self.icon_entity

    @icon.setter
    def icon(self, value):
        if value:
            if not hasattr(self, 'icon_entity'):
                self.icon_entity = Entity(
                    parent=self.model, name=f'buttonicon_entity_{value}',
                    model='quad', texture=value, z=-.1, add_to_scene_entities=False
                )
            else:
                self.icon_entity.texture = value

    def __setattr__(self, name, value):
        if name == 'origin':
            if hasattr(self, 'text_entity') and self.text_entity:
                self.text_entity.world_parent = self.model
                super().__setattr__(name, value)
                self.text_entity.world_parent = self
            else:
                super().__setattr__(name, value)

            if isinstance(self.collider, BoxCollider):
                self.collider = 'box'

        if name == 'on_click':
            self._on_click = value

            if isinstance(value, Sequence):
                value.auto_destroy = False
            return

        if name == 'eternal':
            try:
                self.text_entity.eternal = value
            except AttributeError:
                pass

        try:
            super().__setattr__(name, value)
        except Exception as e:
            return e

    def input(self, key):
        if self.disabled or not self.model or self.hover_highlight_button:
            return

        if key == 'left mouse down':
            if self.hovered:
                self.model.setColorScale(self.pressed_color)
                self.model.setScale(Vec3(self.pressed_scale, self.pressed_scale, 1))

        if key == 'left mouse up':
            if self.hovered:
                self.model.setColorScale(self.highlight_color)
                self.model.setScale(Vec3(self.highlight_scale, self.highlight_scale, 1))
            else:
                self.model.setColorScale(self.color)
                self.model.setScale(Vec3(1, 1, 1))

        if isinstance(self.Key, str):
            if self.partKey == "": #if no partner key
                if self.on_key_press and self.Key is not None and key == self.Key:  # Custom on_key_press handling assuming you have only one key
                    self.on_key_press()
            else:

                if isinstance(self.partKey, str): #if a single partner key like "shift"
                    if self.on_key_press and self.Key is not None and key == self.Key and held_keys[self.partKey]:  # Custom on_key_press handling assuming you have only one key
                        self.on_key_press()

                elif isinstance(self.partKey, list): #if a lot of partner keys and all should be pressed like ["control","shift"]
                    if self.on_key_press and self.Key is not None and key == self.Key and all(held_keys[key] for key in self.partKey):
                        self.on_key_press()

        elif isinstance(self.Key, list):
            if self.partKey == "": #if no partner key
                if self.on_key_press and self.Key is not None and key in self.Key:  # Custom on_key_press handling assuming you have a lot of keys in a list
                    self.on_key_press()
            else:

                if isinstance(self.partKey, str): #if a single partner key like "control"
                    if self.on_key_press and self.Key is not None and key in self.Key and held_keys[self.partKey]:  # Custom on_key_press handling assuming you have a lot of keys in a list
                        self.on_key_press()

                elif isinstance(self.partKey, list):#if a lot of partner keys and all should be pressed like ["control","shift"]
                    if self.on_key_press and self.Key is not None and key in self.Key and all(held_keys[key] for key in self.partKey):
                        self.on_key_press()
        # print(key)


    def on_mouse_enter(self):
        if not self.disabled and self.model:
            self.model.setColorScale(self.highlight_color)
            # if self.hover_highlight:
            #     self.hover_highlight_function()

            if self.highlight_scale != 1:
                self.model.setScale(Vec3(self.highlight_scale, self.highlight_scale, 1))

            if self.on_hover is not None:
                self.on_hover()

            if self.hover_highlight:
                self.hover_highlight_function()

            if self.tool_tip is not None:
                self.tool_tip.enable()

    def on_mouse_exit(self):
        if not self.disabled and self.model:
            self.model.setColorScale(self.color)
            if self.hover_highlight:
                self.hover_unhighlight_function()

            if not mouse.left and self.highlight_scale != 1:
                self.model.setScale(Vec3(1, 1, 1))

            if self.on_unhover is not None:
                self.on_unhover()

            if self.tool_tip is not None:
                self.tool_tip.disable()

    def on_click(self):
        if self.disabled or self.hover_highlight_button:
            return

        action = self._on_click
        if callable(action):
            action()

        elif isinstance(action, Sequence):
            action.start()

        elif isinstance(action, str):
            exec(textwrap.dedent(action))

        # print(self.name)

    def fit_to_text(self, radius=.1, padding=Vec2(Text.size * 1.5, Text.size)):
        if not self.text_entity.text or self.text_entity.text == '':
            return

        self.text_entity.world_parent = scene
        self.original_parent = self.parent
        self.parent = self.text_entity
        self.scale = Vec2(self.text_entity.width, self.text_entity.height) * Text.size * 2
        self.scale += Vec2(*padding)

        self.model = Quad(aspect=self.scale_x / self.scale_y, radius=radius)
        self.parent = self.original_parent
        self.text_entity.world_parent = self


    def hover_highlight_function(self):
        self.highlight_button.color = self.hover_highlight_color
        # print("mouse enter")
    def hover_unhighlight_function(self):
        self.highlight_button.color = color.clear
        # print("mouse exit")

if __name__ == '__main__':
    from GamePlusEditor.ursina import Ursina, application, Tooltip,print_on_screen
    app = Ursina()
    b = Button(text='hello world!', color=color.azure, scale=.25,radius=.2, text_origin=(-.5,0),Key=["a","h"],partKey=["control","shift"],on_key_press = Func(print_on_screen,"all buttons pressed",color = color.black),hover_highlight=True,hover_highlight_size=.8)
    def On_hove():
        print_on_screen("Hovered",(0,.2),(0,0))
    # b.fit_to_text()
    b.on_hover = On_hove
    b.on_click = application.quit # assign a function to the button.
    b.tooltip = Tooltip('exit')
    # print("f" in b.Key)
    if isinstance(b.Key,str):
        print("Str")
    elif isinstance(b.Key,list):
        print("f" in b.Key)
    else:
        print("YEs")
    def input(key):
        print(key)
    # def update():
        # print(held_keys)

    app.run()
