import os
import psutil
import math
from GamePlusEditor.ursina import Text, Vec2, window, camera


def size(size_bytes):
    if size_bytes == 0:
       return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


class MemoryCounter(Text):
    def __init__(self,enabled = True, **kwargs):
        super().__init__(ignore=False)
        self.parent = camera.ui
        self.position = window.bottom_right - Vec2(.025,0)
        self.origin = (0.5, -0.5)
        self.enabled = enabled
        self.always_on_top = True

        self.process = psutil.Process(os.getpid())
        self.i = 0
        self.text = 'Processing'

        for key, value in kwargs.items():
            setattr(self, key, value)

    def update(self):
        self.i += 1
        if self.i > 10:
            self.text = str(size(self.process.memory_info().rss))

            self.i = 0


if __name__ == '__main__':
    from GamePlusEditor.ursina import Ursina
    app = Ursina()
    MemoryCounter()
    '''
    Displays the amount of memory used in the bottom right corner
    '''
    app.run()
