from ursina import Text,color,Entity,camera,Button,Func,destroy,application,Slider
from ursina.prefabs.window_panel import WindowPanel

def ValueToString(value: bool):
    if value:
        return "On"
    else:
        return "Off"

def StringToValue(string: str):
    if string != "":
        return True
    else:
        return False
    
    



def ReplaceText(Entity1,Entity2):
    Entity2Text = Entity2.text
    Entity1Text = Entity1.text
    Entity1.text = Entity2Text
    Entity2.text = Entity1Text
    del Entity1Text
    del Entity2Text
    return 


class CustomWindow():
    def __init__(self,ToEnable,OnEnable,ToEnableOnYes = Func(application.quit),title = "Quit?",text =  "Are you sure you want to quit?",B1text = "No",B2text = "Yes",B1Key = None,B2Key = None):
        self.ToEnable = ToEnable
        self.OnEnable = OnEnable
        self.ToEnableOnYes = ToEnableOnYes
        self.OnEnable()


        self.QuitMenuParentEntity = Entity(parent = camera.ui)

        self.WindowPanelOfQuit = WindowPanel(parent = self.QuitMenuParentEntity,popup = False,scale = (.7,.08),position = (0,.2,-1),title=title,content = [Text(text  = text,origin = (0,0)),Button(color = color.rgba(255,255,255,125),text  = B1text,highlight_color = color.blue,on_click = self.PlayerNotQuitting,Key = B1Key,on_key_press=self.PlayerNotQuitting),Button(color = color.rgba(255,255,255,125),highlight_color = color.blue,Key = B2Key,on_key_press=self.ToEnableOnQuit,text  = B2text,on_click = self.ToEnableOnQuit)])
        self.DarkColorWindowPanel = Button(parent=self.QuitMenuParentEntity, z=1, scale=(999, 999), color=color.black66, highlight_color=color.black66, pressed_color=color.black66)

    def PlayerNotQuitting(self):
        self.ToEnable()
        self.DestroyWindow()

    def ToEnableOnQuit(self):
        self.ToEnableOnYes()
        self.DestroyWindow()
    def DestroyWindow(self):
        for i in range(len(self.QuitMenuParentEntity.children) - 1):
            destroy(self.QuitMenuParentEntity.children[i])
        destroy(self.QuitMenuParentEntity)


def ScaleTransformer(Obj,MinValue,MaxValue):
    a = Slider(min=MinValue,max = MaxValue,default=Obj.scale_x,dynamic=True)
    b = Slider(min=MinValue,max = MaxValue,default=Obj.scale_y,dynamic=True,y = .1)

    def ChangeValue():
        Obj.scale_x = a.value
        Obj.scale_y = b.value
    a.on_value_changed = ChangeValue
    b.on_value_changed = ChangeValue
