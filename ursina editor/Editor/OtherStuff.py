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

def ReplaceValue(Entity1, Entity2, type="color"):
    TempColor1 = getattr(Entity1, type)
    TempColor2 = getattr(Entity2, type)
    setattr(Entity1, type, TempColor2)
    setattr(Entity2, type, TempColor1)
    del TempColor1,TempColor2
    return

def Replacer(Entity1,Entity2):
    Temp1 = Entity2
    Entity2 = Entity1
    Entity1 = Temp1
    del Temp1
    return
def TextToVar(Str: str,ReplaceChar: str = "_"):
    NewStr = Str.lower()
    NewStr = NewStr.replace(" ",ReplaceChar)
    NewStr = NewStr.replace(":","")

    if NewStr.endswith(ReplaceChar):
        NewStr = NewStr[0:-1]
    # print(len(NewStr))
    # TempLen = len(NewStr)
    # for i in range(TempLen):
    #     NewStr += NewStr[i].lower()

    # del TempLen
    return NewStr

print(TextToVar("hew:lwOr X"))

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


def ScaleTransformer(Obj,MinValue:int = 0.01,MaxValue:int =  1):
    a = Slider(min=MinValue,max = MaxValue,default=Obj.scale_x,dynamic=True)
    b = Slider(min=MinValue,max = MaxValue,default=Obj.scale_y,dynamic=True,y = .1)

    def ChangeValue():
        Obj.scale_x = a.value
        Obj.scale_y = b.value
    a.on_value_changed = ChangeValue
    b.on_value_changed = ChangeValue

