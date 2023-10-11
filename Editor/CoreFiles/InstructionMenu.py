from ursina import *
from ursina.color import tint
from ursina.curve import out_cubic

class InstructionMenu(Entity):
    '''Used to show instructions, Used all over the UrsinaEditor'''
    def __init__(self,ToSay: str,OnXClick,DestroyFunc,Title = "Info",killAfter = 5,killIn = 1,WordWrap = 40,Color = tint(color.white,-.2),**kwargs) -> None:
        super().__init__(parent = camera.ui,kwargs=kwargs)
        # self.super = Entity(parent = camera.ui)
        self.Background = Entity(name = "background",parent = self,model = "cube",scale = (.4,.15),color = Color, position = Vec3(1.09, -0.36, -20),always_on_top = True)
        self.CloseButton = Button(name = "button",parent = self.Background,text="X",model = "cube",scale =  (0.029, 0.14),color = color.clear,position = Vec3(0.425, 0.38, 0),on_click = OnXClick)
        self.CloseButton.text_color = tint(color.black,.7)
        self.TitleText = Text(name = "txt",parent = self.Background,text=Title,scale = (3,7),wordwrap = 20,position = Vec3(-0.49, 0.409, 0))

        self.DescriptionText = Text(parent = self.Background,text=ToSay,scale = (2,6),wordwrap = WordWrap,position = Vec3(-0.49, 0.2, 0))


        # self.CloseButton.always_on_top = True
        self.TitleText.always_on_top = True
        self.DescriptionText.always_on_top = True

        invoke(self.kill,killIn,delay = killAfter)
        self.DestroyFunc = DestroyFunc


        self.Background.animate_position(Vec3(0.689, -0.36, -20),.3,curve = out_cubic)

    def show(self,item):
        # item = self.super
        # print(item)
        for i in range(len(item.children)):
            print(f'Name: {item.children[i].name} , pos: {item.children[i].position} , rot: {item.children[i].rotation} , scale; {item.children[i].scale}')
            if item.children[i].children != []:
                self.show(item.children[i])

    def kill(self,sec):
        self.Background.animate_color(color.clear,sec)
        self.CloseButton.animate_color(color.clear,sec)
        self.CloseButton.text_entity.animate_color(color.clear,sec)
        self.DescriptionText.animate_color(color.clear,sec)
        self.TitleText.animate_color(color.clear,sec)
        invoke(self.DestroyFunc,delay = 1)


if __name__ == "__main__":
    ap = Ursina()
    InstructionMenu("Looks like you are new to this editor. You should first watch tutorial to get a full understanding of the editor.",DestroyFunc=Func(print,"yea"),OnXClick=Func(print,"yea"),killIn=100,killAfter = 400)
    ap.run()

