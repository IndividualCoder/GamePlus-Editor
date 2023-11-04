from ursina import *
import sys
from panda3d.core import StencilAttrib,CardMaker,ColorWriteAttrib

class Terminal(Entity):
    def __init__(self,AddTextToTerminalFunc,**kwargs):
        super().__init__(parent = camera.ui)
        self.Texts = []
        self.name = "Terminal"
        self.AddTextToTerminalFunc = AddTextToTerminalFunc

        self.UniversalParentEntity = Entity(parent = self)

        self.Bg = Button(radius = 0,parent = self.UniversalParentEntity,color = color.dark_gray,on_key_press=self.Toogle)
        self.ScrollItemParentEntity = Entity(model = "cube",parent = self.Bg,color = color.clear,radius=0,origin = (0,-.5,0),position =  Vec3(-0.5,-0.48, 3),collider = None,scale_y = .1)

        self.ScrollMax = -.5
        self.ScrollMin = -.5
        # self.Scroller = self.Bg.add_script(Scrollable(max = ,min = ))
        # self.Scroller.entity = self.ScrollItemParentEntity
        # self.Scroller.ToHoverEntity = self.Bg
        self.Bg.input = self.ScrollUpAndDown
        # self.Bg.input = self.input


        for key,value in kwargs.items():
            setattr(self,key,value)

        # self.Toogle()

    def ScrollUpAndDown(self,key):
        if not self.Bg.hovered:
            return


        if key == "scroll up":
            # print('up')
            if round(self.ScrollItemParentEntity.y,2) <= round(self.ScrollMin,2):
                # print("return up")
                return

            self.ScrollItemParentEntity.y -= .01
        if key == "scroll down":
            # print('dwon')
            if round(self.ScrollItemParentEntity.y,2) >= round(self.ScrollMax,2):
                # print("return down")
                return
            self.ScrollItemParentEntity.y += .01

    # def input(self,key):
    #     print(key)
    #     if key == "1":
    #         self.Toogle()

    def Toogle(self):
        self.enabled = not self.enabled



    def AddTextToTerminal(self,text):
        if text == "\n":
            return
        newText = f"{text}"
        self.Texts.insert(0,Text(text= newText,parent = self.ScrollItemParentEntity,x = -.49,y = 1,always_on_top = True,world_scale = (20,20,1)))

        if len(self.Texts) > 1:

            self.ScrollItemParentEntity.scale_y =  self.ScrollItemParentEntity.scale_y + .153
            self.ScrollItemParentEntity.position =  Vec3(-0.5, -0.48, 4)
            self.Texts[0].world_position = Vec3(-8.99, -7.52, 1)
            self.Texts[0].world_scale = Vec3(20, 20, 1)

            for i in range(1,len(self.Texts)):
                self.Texts[i].world_position = (self.Texts[i].world_position.x,self.Texts[i-1].world_position.y + .6,1)
                self.Texts[i].world_scale = Vec3(20, 20, 1)

            if len(self.Texts) > 7:
                self.ScrollMin -= .153

            # self.Scroller.update_target("max",self.Scroller.max + .153)
            # self.Scroller.update_target("max",self.Scroller.max + .03)

    def SetUp(self):
        sys.stdout  = PrintToTerminal(self.AddTextToTerminalFunc)
        self.Bg.highlight_color =  self.Bg.color
        self.Bg.pressed_color =  self.Bg.color

        self.constantOneStencil = StencilAttrib.make(1, StencilAttrib.SCFAlways, StencilAttrib.SOZero, StencilAttrib.SOReplace, StencilAttrib.SOReplace, 1, 0, 1)
        self.stencilReader = StencilAttrib.make(1, StencilAttrib.SCFEqual, StencilAttrib.SOKeep, StencilAttrib.SOKeep, StencilAttrib.SOKeep, 1, 1, 0)

        self.cm = CardMaker("cardmaker")
        self.cm.setFrame(-.6,.99,-.4,-.2)

        self.viewingSquare = render.attachNewNode(self.cm.generate())
        self.viewingSquare.reparentTo(camera.ui)
        self.viewingSquare.setPos(Vec3(0,0,5))

        self.viewingSquare.node().setAttrib(self.constantOneStencil)
        self.viewingSquare.node().setAttrib(ColorWriteAttrib.make(0))

        self.viewingSquare.setBin('background', 0)
        self.viewingSquare.setDepthWrite(0)

        self.ScrollItemParentEntity.node().setAttrib(self.stencilReader)

    def ShowPosTemp(self,Entity):
        sys.__stdout__.write(f"{__file__}:: Name: {Entity.name}, position =  {Entity.position},rotation = {Entity.rotation},scale = {Entity.scale} ")


    def SetUpProperty(self,Entity,val,ToSubOrAdd):
        setattr(Entity,val,getattr(Entity,val) + ToSubOrAdd)

class PrintToTerminal():
    def __init__(self,AddTextFunc):
        self.TextFunc= AddTextFunc

    def write(self, text):
        self.TextFunc(text)

    def flush(self):
        pass


if __name__ == "__main__":
    app = Ursina()
    a = Terminal(lambda : print("hi"))
    a.SetUp()
    print("hi")
    Entity(model = "cube",scale = 10,z = 100,parent = camera.ui)
    app.run()

