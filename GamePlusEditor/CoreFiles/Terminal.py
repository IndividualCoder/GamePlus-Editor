from GamePlusEditor.ursina import *
import sys
from panda3d.core import StencilAttrib,CardMaker,ColorWriteAttrib

class Terminal(Entity):
    '''Terminal used to show things printed'''
    def __init__(self,AddTextToTerminalFunc,**kwargs) -> None:
        super().__init__(parent = camera.ui)
        self.Texts: list = []
        self.name: str = "Terminal"
        self.AddTextToTerminalFunc: function = AddTextToTerminalFunc

        self.UniversalParentEntity: Entity = Entity(parent = self)

        self.Bg: Button = Button(radius = 0,parent = self.UniversalParentEntity,color = color.dark_gray,on_key_press=self.Toogle)
        self.ScrollItemParentEntity:Entity = Entity(model = "cube",parent = self.Bg,color = color.clear,radius=0,origin = (0,-.5,0),position =  Vec3(-0.5,-0.48, 3),collider = None,scale_y = .1)

        self.ScrollMax:int = -.5
        self.ScrollMin:int = -.5
        self.Bg.input: function = self.ScrollUpAndDown


        for key,value in kwargs.items():
            setattr(self,key,value)


    def ScrollUpAndDown(self,key) -> None:
        '''Scrolls the text up and down'''
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

    def Toogle(self) -> None:
        '''Toogles the terminal'''
        self.enabled:bool = not self.enabled



    def AddTextToTerminal(self,text) -> None:
        '''Adds text to the terminal'''
        if text == "\n":
            return
        newText: str = f"{text}"
        self.Texts.insert(0,Text(text= newText,parent = self.ScrollItemParentEntity,x = -.49,y = 1,always_on_top = True,world_scale = (20,20,1)))

        if len(self.Texts) > 1:

            self.ScrollItemParentEntity.scale_y: int | float =  self.ScrollItemParentEntity.scale_y + .153
            self.ScrollItemParentEntity.position: Vec3 =  Vec3(-0.5, -0.48, 4)
            self.Texts[0].world_position:Vec3 = Vec3(-8.99, -7.52, 1)
            self.Texts[0].world_scale:Vec3 = Vec3(20, 20, 1)

            for i in range(1,len(self.Texts)):
                self.Texts[i].world_position: Vec3 = Vec3(self.Texts[i].world_position.x,self.Texts[i-1].world_position.y + .6,1)
                self.Texts[i].world_scale:Vec3 = Vec3(20, 20, 1)

            if len(self.Texts) > 7:
                self.ScrollMin -= .153


    def SetUp(self) -> None:
        '''Sets up the class and overwrites the print funciton'''
        sys.stdout = PrintToTerminal(self.AddTextToTerminalFunc)
        self.Bg.highlight_color: color =  self.Bg.color
        self.Bg.pressed_color: color =  self.Bg.color

        self.constantOneStencil:StencilAttrib = StencilAttrib.make(1, StencilAttrib.SCFAlways, StencilAttrib.SOZero, StencilAttrib.SOReplace, StencilAttrib.SOReplace, 1, 0, 1)
        self.stencilReader:StencilAttrib = StencilAttrib.make(1, StencilAttrib.SCFEqual, StencilAttrib.SOKeep, StencilAttrib.SOKeep, StencilAttrib.SOKeep, 1, 1, 0)

        self.cm: CardMaker = CardMaker("cardmaker")
        self.cm.setFrame(-.6,.99,-.4,-.2)

        self.viewingSquare:NodePath = render.attachNewNode(self.cm.generate())
        self.viewingSquare.reparentTo(camera.ui)
        self.viewingSquare.setPos(Vec3(0,0,5))

        self.viewingSquare.node().setAttrib(self.constantOneStencil)
        self.viewingSquare.node().setAttrib(ColorWriteAttrib.make(0))

        self.viewingSquare.setBin('background', 0)
        self.viewingSquare.setDepthWrite(0)

        self.ScrollItemParentEntity.node().setAttrib(self.stencilReader)


class PrintToTerminal():
    '''Print function is overwritten by this class'''
    def __init__(self,AddTextFunc) -> None:
        self.TextFunc:function = AddTextFunc

    def write(self, text) -> None:
        '''Write function called by `sys.stdout` to print'''
        self.TextFunc(text)

    def flush(self) -> None:
        '''Idk what it does but `sys.stdout` needs this func'''
        ...

if __name__ == "__main__":
    app = Ursina()
    a = Terminal(lambda : print("hi"))
    a.SetUp()
    print("hi")
    Entity(model = "cube",scale = 10,z = 100,parent = camera.ui)
    app.run()

