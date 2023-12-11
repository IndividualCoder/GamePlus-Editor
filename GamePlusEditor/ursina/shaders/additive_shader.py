

if __name__ == '__main__':
    from GamePlusEditor.ursina import *
    from GamePlusEditor.ursina.prefabs.primitives import *
    from panda3d.core import ColorBlendAttrib
    app = Ursina()

    e = Entity(model='sphere', texture='shore', y=2, alpha=.4)
    e.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd))
    ground = GrayPlane(scale=10, y=-2, texture='shore', shader=shader, texture_scale=(10,10))
    EditorCamera()


    app.run()
