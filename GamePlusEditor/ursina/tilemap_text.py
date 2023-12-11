from GamePlusEditor.ursina import Entity, Mesh, load_model, color, camera, Vec3, Vec2



class TilemapText(Entity):
    start_tag = '<'
    end_tag = '>'
    quad_model = None

    def __init__(self, text='', **kwargs):
        super().__init__(parent=camera.ui)

        if not TilemapText.quad_model:
            TilemapText.quad_model = load_model('quad')

        self.model = Mesh(vertices=[], uvs=[], colors=[])
        self.texture = 'Hack_square_64x64'
        self.scale = .025
        self.origin_x = -.5
        self.origin_y = .5
        self.line_height = 1
        self.character_spacing = .5

        self.use_tags = True
        self.start_tag = TilemapText.start_tag
        self.end_tag = TilemapText.end_tag
        self.text_colors = color.colors
        self.text_colors['default'] = color.text_color

        for key, value in kwargs.items():
            setattr(self, key, value)

        self.current_color = self.text_colors['default']

        if text:
            self.text = text

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        # print('set text:', value)
        self._text = value
        self.model.vertices.clear()
        self.model.uvs.clear()
        self.model.colors.clear()

        parsing_tag = False
        lines = value.split('\n')

        for y, line in enumerate(lines):
            x = 0
            for char in line:
                if char == 'space':
                    x += 1
                    continue

                if self.use_tags:
                    if char == '<':
                        parsing_tag = True
                        tag = ''
                        continue

                    elif char == '>':
                        print('tag:', tag)
                        parsing_tag = False
                        if tag in self.text_colors:
                            self.current_color = self.text_colors[tag]
                        continue

                    elif parsing_tag:
                        tag += char
                        continue

                pos = ord(char)
                ascii_table_y = pos // 16
                ascii_table_x = pos - (ascii_table_y * 16)
                # print('x:', ascii_table_x, 'row:', ascii_table_y, 'char:', char)
                self.model.vertices += [Vec3(*v)
                    + Vec3(x*self.character_spacing, -y*self.line_height, 0)
                    + Vec3(.5,-.5,0) # offset quad
                    + Vec3(-len(line) * self.character_spacing * (.5+self.origin_x), len(lines) * self.line_height * (.5-self.origin_y), 0) # center
                    for v in TilemapText.quad_model.vertices]
                self.model.uvs += [(Vec2(*e)+Vec2(ascii_table_x,15-ascii_table_y))/16 for e in TilemapText.quad_model.uvs]
                self.model.colors += [self.current_color for i in range(len(TilemapText.quad_model.vertices))]
                x += 1

        self.model.generate()


    @property
    def origin(self):
        return self._origin

    @origin.setter
    def origin(self, value):
        self._origin = value
        if self.text:
            self.text = self._text


if __name__ == '__main__':
    from GamePlusEditor.ursina import Ursina, dedent, EditorCamera
    app = Ursina()
    # descr = dedent('''
    #     <scale:1.5><orange>Rainstorm<default><scale:1>
    #     Summon a <azure>rain storm <default>to deal 5 <azure>water
    #
    #     damage <default>to <hsb(0,1,.7)>everyone, <default><image:file_icon> <red><image:file_icon> test <default>including <orange>yourself. <default>
    #     Lasts for 4 rounds.''').strip()
    descr = dedent('''
    123456765432

    2134
    4356
    6578

    ''').strip()
    # make_text(descr)
    # s = Sprite('acorn_font_tileset')
    # s.scale *= 3
    # s.texture_scale = (1/16, 1/16)
    # s.texture_offset = (1/16, (16-4)/16)
    Entity(model='quad', scale=.1, color=color.red)
    t = TilemapText(descr, scale=.05)
    # t.text = 'oisefjaeoifj\nopijefoieaj'


    EditorCamera()

    app.run()
