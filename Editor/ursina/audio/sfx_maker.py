from ursina import *


class AudioExplorer(Panel):
    def __init__(self, **kwargs):
        super().__init__(parent=camera.ui, scale=.7, model=Quad(radius=.025),
            position=window.right+Vec2(-.7/2,0), color=color._16)

        self.sound_effects = {}
        self.current_sound_name = ''
        self.current_sound = None

        self.play_button = Button(parent=self, scale=.1, model='circle', color=color.azure, position=(-.5+.025,.5-.025,-.1), origin=(-.5,.5), text='>', on_click=self.play_sound)
        self.text_entity = Text(world_parent=self, text='None', position=self.play_button.position+Vec3(.12,-.05,-.1), origin=(-.5,0))
        self.copy_button = Button(parent=self, scale=(.1,.05), color=color.gray, position=(.5-.025,.5-.05,-.1), origin=(.5,.5), text='copy', on_click=Func(print, 'copy'))

        # original_default_font = Text.default_font
        # Text.default_font = 'VeraMono.ttf'

        for y, name in enumerate(('blip', 'boom', 'coin', 'hurt', 'jump', 'lose', 'powerup', 'teleport')):
            temp_x = 0
            for i in range(1,4):
                full_name = f'{name}_{i}'
                a = Audio(full_name, autoplay=False)
                #
                if not a.clip:
                    destroy(a)
                    continue

                destroy(a)
                #     def change_sound(full_name=full_name):
                #         self.current_sound_name = full_name
                #         self.play_sound()
                #
                #     self.sound_effects[full_name] = change_sound
                #
                # destroy(a)
                width = (Text.get_width(full_name) * 1.25) + .05
                # width = (.02*len(full_name))*1.25
                b = Button(parent=self, y=.5-.155-(y*.06*1.25), x=self.text_entity.x+temp_x, text=full_name,
                    scale=(width, .05*1.25),
                    color=color._64, z=-.1,
                    # text_color=color.light_gray
                    )
                b.model = Quad(radius=.5, aspect=b.scale_x/b.scale_y)
                b.origin = (-.5,.5)
                b.text_entity.scale *= .9
                temp_x += width + .01

                def change_sound(full_name=full_name):
                    self.current_sound_name = full_name
                    self.play_sound()
                b.on_click = change_sound


        self.pitch_slider = Slider(-12, 12, default=0, label='pitch', step=1, dynamic=True, on_value_changed=self.play_sound,
            parent=self, x=-.5+.04, y=-.5+.075, vertical=True, scale=1.5, z=-1)
        self.pitch_slider.bg.color = color._64
        self.volume_slider = Slider(0, 1, default=.5, label='volume', step=.05, dynamic=True, on_value_changed=self.play_sound,
            parent=self, x=-.5+.1, y=-.5+.075, vertical=True, scale=1.5, z=-1)
        self.volume_slider.bg.color = color._64

        # Text.default_font = original_default_font
        # bl = ButtonList(self.sound_effects, parent=self)
        # bl.model = 'wireframe_cube'
        # bl.origin = (-.5,.5)
        # self.bg = Entity(parent=self, model=Quad(.025), z=.1, scale=(.6,.65), origin_x=.5, x=.27, y=.215, collider='box', color=color.black66)


        for key, value in kwargs.items():
            setattr(self, key, value)


    def play_sound(self):
        if not self.current_sound_name:
            return

        new_pitch = pow(1 / 1.05946309436, -self.pitch_slider.value)
        new_pitch = round(new_pitch, 4)

        if self.current_sound:
            self.current_sound.stop()

        self.current_sound = Audio(self.current_sound_name, pitch=new_pitch, volume=self.volume_slider.value)

        # print(self.current_sound)
        self.text_entity.text = f"Audio('{self.current_sound_name}', pitch={new_pitch}, volume={round(self.volume_slider.value,2)})"


if __name__ == '__main__':
    app = Ursina()
    window.color = color.gold
    from time import perf_counter
    t = perf_counter()
    AudioExplorer()
    print('---', perf_counter() - t)

    bg = Sprite('shore', color=color.gray)
    app.run()
