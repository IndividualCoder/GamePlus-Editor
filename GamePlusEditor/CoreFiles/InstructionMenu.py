from GamePlusEditor.ursina import *
from GamePlusEditor.ursina.color import tint
from GamePlusEditor.ursina.curve import out_cubic


class InstructionMenu(Entity):
    '''Used to show instructions'''
    def __init__(self,ToSay: str,Title: str = "Info",killAfter: int | float = 5,killIn: int | float = 1,WordWrap: int = 40,Color: color = tint(color.white,-.2),**kwargs) -> None:
        super().__init__(parent = camera.ui,kwargs=kwargs)
        self.Background: Entity = Entity(name = "background",parent = self,model = "cube",scale = (.4,.15),color = Color, position = Vec3(1.09, -0.36, -20),always_on_top = True)
        self.CloseButton: Button = Button(name = "button",parent = self.Background,text="X",model = "cube",scale =  (0.029, 0.14),color = color.clear,position = Vec3(0.425, 0.38, 0),visible = False)
        self.CloseButton.text_color: color = tint(color.black,.7)
        self.TitleText: Text = Text(name = "txt",parent = self.Background,text=Title,scale = (3,7),wordwrap = 20,position = Vec3(-0.49, 0.409, 0))

        self.DescriptionText: Text = Text(parent = self.Background,text=ToSay,scale = (2,6),wordwrap = WordWrap,position = Vec3(-0.49, 0.2, 0))

        self.TitleText.always_on_top:bool = True
        self.DescriptionText.always_on_top:bool = True

        invoke(self.kill,killIn,delay = killAfter)

        self.Background.animate_position(Vec3(0.689, -0.36, -20),.3,curve = out_cubic)

    def kill(self,sec) -> None:
        '''Kills the instruction'''
        self.Background.animate_color(color.clear,sec)
        self.CloseButton.animate_color(color.clear,sec)
        self.CloseButton.text_entity.animate_color(color.clear,sec)
        self.DescriptionText.animate_color(color.clear,sec)
        self.TitleText.animate_color(color.clear,sec)
        invoke(self.CloseButton.on_click,delay = 1)

    def Up(self,Last) -> None:
        '''Makes the menu go up relative to the menu under it '''
        self.animate_position(Vec3(self.x,self.y + Last.Background.scale_y  + .03,self.z),duration=.1,curve = out_cubic)

if __name__ == "__main__":
    ap = Ursina()
    InstructionMenu("Looks like you are new to this editor. You should first watch tutorial to get a full understanding of the editor.",DestroyFunc=Func(print,"yea"),OnXClick=Func(print,"yea"),killIn=100,killAfter = 400)
    ap.run()

