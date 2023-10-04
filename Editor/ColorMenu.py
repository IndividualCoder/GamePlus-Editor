from ursina import *

class ColorMenu(Entity):
    '''Not done yet ;)'''
    def __init__(self,EntityToColor,DestoryFunc,**kwargs):
        super().__init__(parent = camera.ui,*kwargs)
        self.EntityToColor = EntityToColor
        self.ColorButton = Button(parent = self,color = self.EntityToColor.color)

        # self.bg = Button(model = "cube",scale = 99,parent = camera.ui,color = color.black66,highlight_color = color.black66,clicked_color = color.black66,z = -9,on_click = DestoryFunc)
        # self.Menu = Entity(model = "cube",z = -8,render_queue = 10)



    def UpdateColor(self):
        self.EntityToColor.color = color.hsv



if __name__ == "__main__":
    app  = Ursina()
    ColorMenu(None,Func(print_on_screen,'hi',position = (-.1,0)))
    app.run()



