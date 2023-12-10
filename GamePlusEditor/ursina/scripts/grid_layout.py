from ursina import *


def grid_layout(l, max_x=8, max_y=8, spacing=(0,0,0), origin=(-.5,.5,0), offset=(0,0,0)):
    if len(origin) == 2:
        origin += (0,)
    if len(offset) == 2:
        offset += (0,)
    if not isinstance(l, list):
        print('error: grid_layout input must be a list or tuple, not', l.__class__.__name__)
        return
    x, y, z = 0, 0, 0

    dimensions = l[0].bounds.size
    direction = [-e*2 for e in origin]
    direction = [1 if e == 0 else e for e in direction]
    # print(direction)
    row = list()

    for i, e in enumerate(l):
        e.position = (
            x * dimensions[0] * direction[0],
            y * dimensions[1] * direction[1],
            z * dimensions[2] * direction[2]
        )
        e.position += offset
        e.origin = origin
        row.append(e)

        x += 1
        if x >= max_x:
            y += 1
            x = 0
            # center row
            if origin[0] == 0:
                for e in row:
                    e.x -= e.bounds.size.x * len(row) / 2 - e.bounds.size.x / 2
            row.clear()

        if y >= max_y:
            z += 1
            y = 0

        e.x *= 1 + spacing[0]
        e.y *= 1 + spacing[1]

    # center last row
    if origin[0] == 0:
        for e in row:
            e.x -= e.bounds.size.x * len(row) / 2 - (e.bounds.size.x / 2)

if __name__ == '__main__':
    app = Ursina()

    center = Entity(model='quad', scale=.1, color=color.red)
    p = Entity()
    for i in range(4*5):
        b = Button(parent=p, model='quad', scale=Vec2(.2,.1), text=str(i), color=color.tint(color.random_color(),-.6))
        b.text_entity.scale=1
    t = time.time()
    grid_layout(p.children, max_x=7, max_y=10, origin=(0, .5), spacing=(.15, 0))
    center = Entity(parent=camera.ui, model=Circle(), scale=.005, color=color.lime)
    EditorCamera()
    print(time.time() - t)

    # test
    for e in [(-.5,.5), (0,.5), (.5,.5), (-.5,0), (0,0), (.5,0), (-.5,-.5), (0,-.5), (.5,-.5)]:
        Button(
            text='*',
            model='quad',
            text_origin=e,
            scale=.095,
            origin=(-.5,.5),
            position = window.top_left + Vec2(*e)*.2 + Vec2(.1,-.1),
            tooltip=Tooltip(str(e)),
            on_click=Func(grid_layout, p.children, max_x=7, max_y=10, origin=e, spacing=(.15, 0))
        )



    app.run()
