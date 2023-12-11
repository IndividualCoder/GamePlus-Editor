from GamePlusEditor.ursina import *


class TerrainSystem(Entity):
    def __init__(self, height_values, subsection_dimensions=[64, 64], player=None, **kwargs):
        super().__init__(**kwargs)

        self.subsection_dimensions = subsection_dimensions
        w = len(height_values)
        h = len(height_values[0])
        self.subsections = [[None for y in range(h)] for x in range(w)]
        self.player = player

        for y in range(h // subsection_dimensions[1]):
            for x in range(w // subsection_dimensions[0]):
                print('-----', x,y)
                hv = [[None for y in range(64)] for x in range(64)]

                for __y in range(64):
                    for __x in range(64):
                        hv[__x][__y] = height_values[63*x + __x][63*y + __y]

                print(hv)
                tile = Entity(parent=self,
                    model=Terrain(height_values=hv),
                    x=x*63, z=y*63, scale=Vec3(64, 1, 64),
                    texture_scale=(1/4, 1/2),
                    texture_offset=(x/4, y/2),
                    texture='heightmap_1'
                    )


                self.subsections[x][y] = tile

    def update(self):
        if not self.player:
            return





if __name__ == '__main__':
    app = Ursina()
    from GamePlusEditor.ursina.models.procedural.terrain import texture_to_height_values
    hv = texture_to_height_values('heightmap_1', skip=1)
    TerrainSystem(hv, scale_y=32)

    EditorCamera()
    app.run()
