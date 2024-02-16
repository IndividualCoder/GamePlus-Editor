from GamePlusEditor.ursina import *
from panda3d.core import DirectionalLight

class DirectLight(Entity):
    def __init__(self,LightNum, **kwargs):
        super().__init__(**kwargs)
        self._DirectionalLight = DirectionalLight(f"DLight {LightNum}")
        self._DirectionalLightNodePath = render.attachNewNode(self._DirectionalLight)

    def SetUp(self):
        render.setLight(self._DirectionalLightNodePath)

    def on_destroy(self):
        print("on_destroy")
        render.clearLight(self._DirectionalLightNodePath)


if __name__ == "__main__":
    app = Ursina()

    enti = DirectLight(2)
    enti2 = DirectLight(2)

    destroy(enti)

    app.run()