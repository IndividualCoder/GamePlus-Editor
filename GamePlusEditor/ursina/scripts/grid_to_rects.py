

def volume(e):
    return e[0] * e[1]


def create_shapes(size_x, size_y):
    sizes = [(size_x, size_y) for i in range(size_x*size_y)]

    i = 0
    for x in range(size_x):
        for y in range(size_y):
            sizes[i] = (x+1,y+1)
            i += 1
    sizes.sort(key=volume, reverse=True)
    return sizes


def grid_to_rects(grid, solid_value=1):
    '''
    Converts a 2d grid into rects by finding the biggest shapes first.
    Parameters: grid(2D array), grid size x(int), grid_size_y(int)
    Returns: a list of (position, size)
    '''
    grid_size_x = len(grid)
    grid_size_y = len(grid[0])

    shapes = create_shapes(grid_size_x, grid_size_y)
    filled = [[0 for y in range(grid_size_y)] for x in range(grid_size_x)]

    # find number of blocks so we can exit early when all have been found
    num_solid_blocks = 0
    for x in range(grid_size_x):
        for y in range(grid_size_y):
            if grid[x][y] == solid_value:
                num_solid_blocks += 1


    rects = []

    for shape in shapes:
        w, h = shape
        # print('checking shape:', w,h,d)
        # check at each position
        for x in range(grid_size_x - w + 1):
            for y in range(grid_size_y - h + 1):
                if filled[x][y] == solid_value:
                    continue

                if shape_fits_in_grid(grid, x,y, filled, grid_size_x, grid_size_y, w, h, solid_value):
                    rects.append(((x,y), shape))

                    for _x in range(w):
                        for _y in range(h):
                            filled[x+_x][y+_y] = 1
                            num_solid_blocks -= 1

                    if num_solid_blocks == 0:
                        return rects

    return rects


def shape_fits_in_grid(grid, start_x, start_y, filled, grid_size_x, grid_size_y, shape_w, shape_h, solid_value):
    for x in range(shape_w):
        for y in range(shape_h):
            if filled[start_x+x][start_y+y]:
                return False
            if not grid[start_x+x][start_y+y] == solid_value:
                return False
    return True


if __name__ == '__main__':
    from time import perf_counter

    def string_to_2d_array(str):
        # print(str)

        lines = str.split('\n')
        lines.reverse()
        w = len(lines[0])
        h = len(lines)
        # print('----', lines)

        grid =  [[0 for y in range(h)] for x in range(w)]
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                grid[x][y] = int(char)

        # print('----', grid)

        return grid

    from textwrap import dedent
    grid = string_to_2d_array(dedent('''
        0002222222222222
        2222222211111112
        2222222211221112
        2222222111221112
        2222222211221112
        2221112222222112
        2221112222222112
        2221112222222111
        2222222222222111
        ''').strip())



    print(grid)

    t = perf_counter()
    rects = grid_to_rects(grid, solid_value=1)
    print('--------', perf_counter() - t)
    print(rects)


    from GamePlusEditor.ursina import *
    app = Ursina()

    entities = []
    for e in rects:
        pos, scale = e
        entities.append(Entity(model='quad', origin=(-.5,-.5,-.5), position=pos, scale=scale, texture='white_cube'))


    EditorCamera()
    app.run()
