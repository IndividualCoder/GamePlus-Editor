from ursina import Text,color,Entity,camera,Button,Func,destroy,application,Slider,Sequence
from ursina.prefabs.window_panel import WindowPanel
import os

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

def PrepareForRecentProjects(String: str):
    String = String.replace("Project","")
    String = String.replace("Networking","")
    String = String.replace("Current","")
    String = String.replace("Quality"," quality")
    # String = String.replace("Base"," base")
    String = String.replace("Platform"," platform") 
    String = String.capitalize()
    return String


def FormatForSaving(string: str):
    string = string.replace("\\","/")
    string = string.replace("\\\\","/")
    string = string.replace("Editor","")
    return string


def CurrentFolderNameReturner():
    return os.path.dirname(os.path.abspath(__file__))
# print(CurrentFolderNameReturner())
# print(TextToVar("hew:lwOr X"))

class CustomWindow():
    def __init__(self,ToEnable,OnEnable,ToEnableOnYes = Func(application.quit),title = "Quit?",text =  "Are you sure you want to quit?",B1text = "No",B2text = "Yes",B1Key = None,B2Key = None,content = None,CalcAndAddTextLines = True,ToAddHeight = 0):
        self.ToEnable = ToEnable
        self.OnEnable = OnEnable
        self.ToEnableOnYes = ToEnableOnYes
        if content is not None:
            for button in range(len(content)):
                if hasattr(content[button],"click_to_destroy"):
                    content[button].on_click = self.PlayerNotQuitting

        self.OnEnable()


        self.QuitMenuParentEntity = Entity(parent = camera.ui)
        if content is None:
            self.WindowPanelOfQuit = WindowPanel(parent = self.QuitMenuParentEntity,popup = True,scale = (.7,.08),position = (0,.2,-1),title=title,content = [Text(text  = text,origin = (0,0)),Button(color = color.rgba(255,255,255,125),text  = B1text,highlight_color = color.blue,on_click = self.PlayerNotQuitting,Key = B1Key,on_key_press=self.PlayerNotQuitting),Button(color = color.rgba(255,255,255,125),highlight_color = color.blue,Key = B2Key,on_key_press=self.ToEnableOnQuit,text  = B2text,on_click = self.ToEnableOnQuit)],CalcAndAddTextLines = CalcAndAddTextLines,ToAddHeight = ToAddHeight)
            self.DarkColorWindowPanel = Button(parent=self.QuitMenuParentEntity, z=1, scale=(999, 999), color=color.black66, highlight_color=color.black66, pressed_color=color.black66)
        if content is not None:
            self.WindowPanelOfQuit = WindowPanel(parent = self.QuitMenuParentEntity,popup = True,scale = (.7,.08),position = (0,.3,-30),title=title,content = content,CalcAndAddTextLines = CalcAndAddTextLines,ToAddHeight = ToAddHeight,render_queue = 100)
            self.DarkColorWindowPanel = Button(parent=self.QuitMenuParentEntity, z=-29, scale=(999, 999), color=color.rgba(0,0,0,0), highlight_color=color.rgba(0,0,0,0), pressed_color=color.rgba(0,0,0,0),render_queue = 99)

    def PlayerNotQuitting(self):
        self.ToEnable()
        self.DestroyWindow()

    def ToEnableOnQuit(self):
        self.ToEnableOnYes()
        self.DestroyWindow()

    def DestroyWindow(self):
        for i in range(len(self.QuitMenuParentEntity.children) - 1):
            destroy(self.QuitMenuParentEntity.children[i])
        destroy(self.DarkColorWindowPanel)
        destroy(self.QuitMenuParentEntity)


def ScaleTransformer(Obj,MinValue:int = 0.01,MaxValue:int =  1):
    a = Slider(min=MinValue,max = MaxValue,default=Obj.scale_x,dynamic=True)
    b = Slider(min=MinValue,max = MaxValue,default=Obj.scale_y,dynamic=True,y = .1)

    def ChangeValue():
        Obj.scale_x = a.value
        Obj.scale_y = b.value
    a.on_value_changed = ChangeValue
    b.on_value_changed = ChangeValue



from ursina import ButtonList,mouse

class AssetMenu(Entity):
    def __init__(self):
        super().__init__(parent=camera.ui, enabled=True, z=-2, name=__class__.__name__)
        self.button_list = ButtonList({}, parent=self, font='VeraMono.ttf', x=-.25*.75, scale=.75)
        self.bg = Entity(parent=self.button_list, model='quad', collider='box', color=color.black33, on_click=self.disable, z=.1, scale=100)

    def on_enable(self):
        if not self.asset_names:
            print('no texture assets found')
            # return
        asset_dict = {name : Func(self.on_select_asset, name) for name in self.asset_names}
        self.button_list.button_dict = asset_dict
        self.button_list.y = len(asset_dict) / 2 * self.button_list.button_height * Text.size
        self.button_list.x = mouse.x
        self.button_list.y = mouse.y


class ModelMenu(AssetMenu):
    def on_enable(self):
        # self.model_names = [e.stem for e in application.internal_models_compressed_folder.glob('**/*.ursinamesh')]
        self.asset_names = ['None', 'cube', 'sphere', 'plane']
        for file_type in ('.bam', '.obj', '.ursinamesh'):
            self.asset_names += [e.stem for e in application.asset_folder.glob(f'**/*{file_type}') if not 'animation' in e.stem]

        super().on_enable()

    def on_select_asset(self, name):
        if name == 'None':
            name = None

        changes = []
        for e in LEVEL_EDITOR.selection:
            index = LEVEL_EDITOR.entities.index(e)
            if not e.model:
                changes.append((index, 'model', None, name))
            else:
                changes.append((index, 'model', e.model.name, name))

        for e in LEVEL_EDITOR.selection:
            e.model = name
            if name == 'cube':
                e.collider = 'cube'
            else:
                e.collider = None

        LEVEL_EDITOR.menu_handler.state = 'None'
