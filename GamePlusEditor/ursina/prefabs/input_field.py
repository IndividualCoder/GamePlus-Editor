# from enum import Enum

class ContentTypes:
    int = '0123456789'
    float = int + '.,'
    math = float + '+-*/'
    int_math = int + '+-*/'

from GamePlusEditor.ursina import *

class InputField(Button):
    def __init__(self, default_value='', label='', max_lines=1, character_limit=24, placeholder='',submit_on = None,enable_slider = True,escape_active = False, **kwargs):
        if not 'scale' in kwargs and not 'scale_x' in kwargs and not 'scale_y' in kwargs:
            kwargs['scale'] = (.5, Text.size*2*max_lines)
        super().__init__(highlight_scale=1, pressed_scale=1, highlight_color=color.black, **kwargs)



        for key, value in kwargs.items():
            # if 'scale' in key:
            setattr(self, key, value)

        if "enter_active" in kwargs:
            self.enter_active = True

        self.escape_active = escape_active
        self.default_value = default_value
        self.limit_content_to = None
        self.hide_content = False
        self.PlaceHolder = placeholder

        self.next_field = None
        self.submit_on = submit_on
        if not "on_submit" in kwargs:
            self.on_submit = self.MakeUnActive
        else:
            self.on_submit = kwargs['on_submit']

        self.on_value_changed = None
        self.horizontal_slider = enable_slider
        self.max_lines = max_lines
        if "text_scale" in kwargs:
            self.text_field = TextField(world_parent=self, x=-.45, y=.3, z=-.1, max_lines=max_lines, character_limit=character_limit, register_mouse_input=True,text_scale= kwargs['text_scale'],cursor_y = kwargs["cursor_y"])
        else:
            self.text_field = TextField(world_parent=self, x=-.45, y=.3, z=-.1, max_lines=max_lines, character_limit=character_limit, register_mouse_input=True)
        self.placeholder_color = color.rgba(255,255,255,120)
        self.placeholder = Text(parent = self,position=self.text_field.position,color = self.placeholder_color,scale_x = self.text_field.scale_x * 1.25,scale_y = self.text_field.scale_y * 1.25,font = 'VeraMono.ttf')
        destroy(self.text_field.bg)
        self.text_field.bg = self

        self.input(key = '7')

        def render():
            if self.limit_content_to:
                org_length = len(self.text_field.text)
                self.text_field.text = ''.join([e for e in self.text_field.text if e in self.limit_content_to])
                self.text_field.cursor.x -= org_length - len(self.text_field.text)
                self.text_field.cursor.x = max(0, self.text_field.cursor.x)

            if self.hide_content:
                replacement_char = '*'
                if isinstance(self.hide_content, str):
                    replacement_char = self.hide_content

                self.text_field.text_entity.text = replacement_char * len(self.text_field.text)
                return

            if self.on_value_changed and not self.text_field.text_entity.text == self.text_field.text:
                self.on_value_changed()

            if self.text_field.text_entity.width > self.scale_x and self.max_lines > 1:
                self.text_field.get_next_line()                

            # print('aoue')

            self.text_field.text_entity.text = self.text_field.text
        self.text_field.render = render

        self.text_field.scale *= 1.25

        if self.default_value:
            self.text_field.text = default_value
        # else:
        #     self.text_field.text = placeholder
        #     self.text_field.text_entity.color = color.rgba(255, 255, 255, 100)

        self.text_field.render()
        self.text_field.shortcuts['indent'] = ('')
        self.text_field.shortcuts['dedent'] = ('')

        # self.active = False
        if self.PlaceHolder:
            self.placeholder.text  = self.PlaceHolder

        if label:
            self.label = Text(str(label) + ':', parent=self, position=self.text_field.position, scale=1.25)
            self.text_field.x += 0.1 * (len(str(label)) + 1.0) / 6.0

        for key, value in kwargs.items():
            setattr(self, key, value)

    def input(self, key):
        if key == 'tab' and self.text_field.cursor.y >= self.text_field.max_lines-1 and self.active:
            self.active = False
            if self.next_field:
                mouse.position = self.next_field.get_position(relative_to=camera.ui)
                invoke(setattr, self.next_field, 'active', True, delay=.01)
            return
        if self.text_field.text == "":
            self.EnablePlaceholder()
        else:
            self.DisablePlaceholder()

        # if self.escape_active and self.active and key == "escape":
        #     self.FlipActive()
        if isinstance(self.submit_on, str):
            if self.active and self.submit_on and key == self.submit_on and self.on_submit:
                # print("Submitted")
                self.on_submit()
                if hasattr(self,"enter_active"):
                    self.MakeUnActive()
                # self.active = False
                return
        elif isinstance(self.submit_on, list):
            if self.active and self.submit_on and key in self.submit_on and self.on_submit:
                # print("Submitted")
                self.on_submit()
                if hasattr(self,"enter_active"):
                    self.MakeUnActive()
                # self.active = False
                return



    @property
    def text(self):
        return self.text_field.text

    @text.setter
    def text(self, value):
        self.text_field.text = ''
        self.text_field.cursor.position = (0, 0)
        self.text_field.add_text(value, move_cursor=True)
        self.text_field.render()

    @property
    def text_color(self):
        return self.text_field.text_entity.color

    @text_color.setter
    def text_color(self, value):
        self.text_field.text_entity.color = value

    @property
    def active(self):
        return self.text_field.active

    @active.setter
    def active(self, value):
        self.text_field.active = value

    def EnablePlaceholder(self):
        self.placeholder.enable()
    
    def DisablePlaceholder(self):
        self.placeholder.disable()
    
    def MakeActive(self):
        self.active = True

    def MakeUnActive(self):
        self.active = False


if __name__ == '__main__':
    app = Ursina()
    # window.fullscreen_size = (1366, 768)
    background = Entity(model='quad', texture='pixelscape_combo', parent=camera.ui, scale=(camera.aspect_ratio,1), color=color.white)
    gradient = Entity(model='quad', texture='vertical_gradient', parent=camera.ui, scale=(camera.aspect_ratio,1), color=color.hsv(240,.6,.1,.75))

    username_field = InputField(y=-.12, limit_content_to='abcdefghijklmnopqrstuvwxyz1234567890',placeholder =  "Enter your name")
    password_field = InputField(y=-.18, hide_content='NYT',on_active = Func(print,"Activated"),scale_y = .15,escape_active=True)
    username_field.next_field = password_field
    
    # scale_x_slider = Slider(min = 1,max=100,default=username_field.placeholder.scale_x,text="Scale x",dynamic=True)

    # scale_y_slider = Slider(min = 1,max=100,default=username_field.placeholder.scale_y,y = -0.3,text="Scale y",dynamic=True)

    # def Renew():
    #     username_field.placeholder.scale_x = scale_x_slider.value
    #     username_field.placeholder.scale_y = scale_y_slider.value
    #     print(f"x: {scale_x_slider.value},y: {scale_y_slider.value}")
    # scale_x_slider.on_value_changed = Renew
    # scale_y_slider.on_value_changed = Renew

    def submit():
        print('ursername:', username_field.text)
        print('password:',  password_field.text)
        username_field.enable()
    Button('Login', scale=.1, color=color.cyan.tint(-.4), y=-.26, on_click=submit).fit_to_text()
    # username_field.on_value_changed = submit
    app.run()
