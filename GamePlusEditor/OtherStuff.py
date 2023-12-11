'''Simple small function that are used all over the editor'''
from GamePlusEditor.ursina import Text,color,Entity,camera,Button,Func,destroy,application,Slider
from GamePlusEditor.ursina.prefabs.window_panel import WindowPanel
import os
import shutil
import webbrowser


def ValueToString(value: bool):
    '''Returns a On if value is True else Off'''
    if value:
        return "On"
    else:
        return "Off"
def BoolInverter(value: bool):
    '''Returns a True if value is False else False'''
    if value:
        return False
    else:
        return True

def StringToValue(string: str):
    '''Returns True if given str is not empty, else False'''
    if string != "":
        return True
    else:
        return False

def ReplaceValue(Entity1, Entity2, type="color"):
    '''Replaces a value between Entity1 and Entity 2, type is by default color so it means the color will be swapped. it can be any variable'''
    TempColor1 = getattr(Entity1, type)
    TempColor2 = getattr(Entity2, type)
    setattr(Entity1, type, TempColor2)
    setattr(Entity2, type, TempColor1)
    del TempColor1,TempColor2
    return

def Replacer(Entity1,Entity2):
    '''Replaces 2 entities, not the value! if I want to replace entity1.children[2] and entity2.children[1], I can do it with this func'''
    Temp1 = Entity2
    Entity2 = Entity1
    Entity1 = Temp1
    del Temp1
    return

def TextToVar(Str: str,ReplaceChar: str = "_"):
    NewStr = Str.lower()
    NewStr = NewStr.replace(" ",ReplaceChar)
    NewStr = NewStr.replace(":","")
    NewStr = NewStr.replace("render/","") # just for parent 
    if NewStr.endswith(ReplaceChar):
        NewStr = NewStr[0:-1]
    NewStr = NewStr.replace("position_", "")
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
    '''Formats a given by first removing all backslashs, Usually used to format the str to save'''
    string = string.replace("\\","/")
    string = string.replace("\\\\","/")
    return string


def CurrentFolderNameReturner():
    '''Returns the name of the current folder and to prevent confusion, replaces all backslashes with forward slashes'''
    return os.path.dirname(os.path.abspath(__file__)).replace("\\","/")

def DeleteProject(Name,Path):
    '''The name explains it all'''
    shutil.rmtree(f"{Path}/{Name}")

def MultiFunctionCaller(*FunctionList,ToReturn = None):
    '''Call as many function at once as you want. Can use the sequence but it seems like it can be called only once. Message me if it's not the case'''
    for Function in FunctionList:
        Function()
    return ToReturn

def RecursivePerformer(Entity,ToPerform:str = "enable",kwargs: dict = {},BasicFunc = True):
    """Performs a fucntion to an entity and its all children recursively.\n
    The Entity can also be a list.\n
    The second input is ToPerform which by default performs the enable action to the entities but the action can be anything\n
    but remember, if ToPerform returns something, it will be ignored by this function and None will be returned\n
    Keyword arguments can also be defined to give to the ToPerform function. Scroll to read more\n
    The last arg is BasicFunc, it means, does the entity have a func (like this: enity.func) if it is False, it will be performed like this:\n\t(func(entity)) the entity will be given as an argument"""

    if BasicFunc:
        if isinstance(Entity,list):
            for j in range(len(Entity)):
                ToRunFunc = getattr(Entity[j],ToPerform)
                ToRunFunc(*kwargs)
                for i in range(len(Entity[j].children)):
                    ToRunFunc = getattr(Entity[j].children[i],ToPerform)
                    ToRunFunc(*kwargs)
                    if Entity[j].children[i].children != []:
                        RecursivePerformer(Entity[j].children[i],ToPerform=ToPerform,kwargs=kwargs)
            return


        ToRunFunc = getattr(Entity,ToPerform)
        ToRunFunc(*kwargs)

        for i in range(len(Entity.children)):
            ToRunFunc = getattr(Entity.children[i],ToPerform)
            ToRunFunc(*kwargs)
            if Entity.children[i].children != []:
                RecursivePerformer(Entity.children[i],ToPerform=ToPerform,kwargs=kwargs)

        return

    if isinstance(Entity,list):
        for j in range(len(Entity)):
            ToPerform(Entity[j],*kwargs)
            for i in range(len(Entity[j].children)):
                ToPerform(Entity[j].children[i],*kwargs)
                if Entity[j].children[i].children != []:
                    RecursivePerformer(Entity[j].children[i],ToPerform=ToPerform,kwargs=kwargs,BasicFunc=BasicFunc)
        return


    ToPerform(Entity,*kwargs)

    for i in range(len(Entity.children)):
        ToPerform(Entity.children[i],*kwargs)
        if Entity.children[i].children != []:
            RecursivePerformer(Entity.children[i],ToPerform=ToPerform,kwargs=kwargs,BasicFunc=BasicFunc)

    return

def OpenBrowser(url: str):
    '''Opens a specific url in the default browser. Like https://www.youtube.com'''
    webbrowser.open(url)

class CustomWindow():
    def __init__(self,ToEnable,OnEnable,ToEnableOnYes = Func(application.quit),title = "Quit?",text =  "Are you sure you want to quit?",B1text = "No",B2text = "Yes",B1Key = None,B2Key = None,content = None,CalcAndAddTextLines = True,ToAddHeight = 0,Queue = 0):
        self.ToEnable = ToEnable
        self.OnEnable = OnEnable
        self.ToEnableOnYes = ToEnableOnYes
        if content is not None:
            for button in range(len(content)):
                if hasattr(content[button],"click_to_destroy"):
                    content[button].on_click = self.PlayerNotQuitting
        if self.OnEnable is not None:
            self.OnEnable()


        self.QuitMenuParentEntity = Entity(parent = camera.ui)
        if content is None:
            self.WindowPanelOfQuit = WindowPanel(parent = self.QuitMenuParentEntity,popup = True,scale = (.7,.08),position = (0,.2,-1),title=title,content = [Text(text  = text,origin = (0,0)),Button(color = color.rgba(255,255,255,125),text  = B1text,highlight_color = color.blue,on_click = self.PlayerNotQuitting,Key = B1Key,on_key_press=self.PlayerNotQuitting),Button(color = color.rgba(255,255,255,125),highlight_color = color.blue,Key = B2Key,on_key_press=self.ToEnableOnQuit,text  = B2text,on_click = self.ToEnableOnQuit)],CalcAndAddTextLines = CalcAndAddTextLines,ToAddHeight = ToAddHeight)
            self.DarkColorWindowPanel = Button(parent=self.QuitMenuParentEntity, z=1, scale=(999, 999), color=color.black66, highlight_color=color.black66, pressed_color=color.black66)

        if content is not None:
            self.WindowPanelOfQuit = WindowPanel(parent = self.QuitMenuParentEntity,popup = True,scale = (.7,.08),position = (0,.3,-203),title=title,content = content,CalcAndAddTextLines = CalcAndAddTextLines,ToAddHeight = ToAddHeight,render_queue = Queue)
            self.DarkColorWindowPanel = Button(parent=self.QuitMenuParentEntity, scale=(999, 999), color=color.rgba(0,0,0,0), highlight_color=color.rgba(0,0,0,0), pressed_color=color.rgba(0,0,0,0),position = (0,0,-202),always_on_top = True)

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



