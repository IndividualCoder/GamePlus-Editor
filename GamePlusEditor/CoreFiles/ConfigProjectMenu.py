import sys
import os

# Make the main to 'Editor' so we can access the files of the 'Editor' folder
editor_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.append(editor_directory)

from GamePlusEditor.ursina import *
import json
from GamePlusEditor.OtherStuff import CurrentFolderNameReturner
from GamePlusEditor.CoreFiles.TrueFalseIndicator import TrueFalseIndicator

class ConfigProjectManager(Entity):
    '''Manages a simple menu shown when you configure your project'''

    def __init__(self,Parent,Path,CancelClick,ToSaveDataFunc = Func(print,"hi")):
        super().__init__(parent = Parent)
        self.ProjectPath: str = Path
        self.CancelClick: function = CancelClick
        self.ConfigProjectStateList: tuple = (("Low","Medium","High"),("Python","Ursa-visor"),("True","False"),("windows","mac","ios","Linux","android"),("FPC","TPC","TopDown","Platformer","FPCTPC"))
        self.ToSaveDataFunc: function = ToSaveDataFunc
        self.CurrentProjectName: str = None

        self.ProjectStateChangerButtons: list = []

        self.UniversalParentEntity: Entity = Entity(parent = self,enabled = False)
        self.BackGround: Entity = Entity(parent = self.UniversalParentEntity,model = "cube",scale = 10,color = color.black66)
        
        self.CancelButton: Button = Button(parent = self.UniversalParentEntity,name = "cancel button",text = "Cancel",position = Vec3(-0.74, 0.42, 0) , rotation = Vec3(0, 0, 0) , scale = Vec3(0.270001, 0.13, 1),on_click = self.Close)
        self.SaveButton: Button = Button(parent = self.UniversalParentEntity,name = "save buton",text = "Save and exit",position = Vec3(-0.46, 0.42, 0) , rotation = Vec3(0, 0, 0) , scale = Vec3(0.270001, 0.130001, 1),on_click = self.ConfigProjectAsSettings)


    def Show(self,Name: str) -> None:
        '''Shows the menu\nGets the latest data from secondary memory'''

        with open(f"{self.ProjectPath}/{Name}/Game settings.txt","r")  as File:
            self.GameSettings: dict = json.load(File)
            self.ProjectName: str = Name
        for i,j in enumerate(self.GameSettings):
            self.NameText: Text = Text(f"{j}:",parent = self.UniversalParentEntity,y = .32-i*.1,x = -.5,scale = 2,z = -1)
            self.ProjectStateChangerButtons.append(TrueFalseIndicator(parent = self.NameText,DefaultState=str(self.GameSettings[j]),StateList= self.ConfigProjectStateList[i],position = (.5,0,0),scale = (.2,.025,1)))
        self.NameText: Text = Text(f"Name: ",parent = self.UniversalParentEntity,y = .32-5*.1,x = -.5,scale = 2,z = -1)
        self.ProjectStateChangerButtons.append(InputField(parent = self.NameText,default_value=Name,position = (.5,0,0),scale = (.2,.025,1),active = False,))

    def ConfigProjectAsSettings(self) -> None:
        '''Changes the project to desired\nReturns nothing but saves the data in the file'''
        if hasattr(self,"GameSettings"):
            for i,j in enumerate(self.GameSettings):
                if self.ProjectStateChangerButtons[i].Button.text.lower() in ['true',"false"]:
                    if self.ProjectStateChangerButtons[i].Button.text.lower() == "true":
                        self.GameSettings[j] = True
                    else:
                        self.GameSettings[j] = False
                else:
 
                    self.GameSettings[j] = self.ProjectStateChangerButtons[i].Button.text
            if self.ProjectStateChangerButtons[-1].text != self.ProjectName:
                os.rename(f"{CurrentFolderNameReturner()}/Current Games/{self.ProjectName}",f"{CurrentFolderNameReturner()}/Current Games/{self.ProjectStateChangerButtons[-1].text}")
                self.ProjectName  = self.ProjectStateChangerButtons[-1].text

            with open(f'{self.ProjectPath}/{self.ProjectName}/Game settings.txt',"w") as File:
                json.dump(self.GameSettings,File)
            self.ToSaveDataFunc(Name = self.CurrentProjectName,Replace = self.ProjectName)

            self.Close()

    def Close(self) -> None:
        '''Closes the menu'''
        if hasattr(self,"GameSettings"):
            del self.GameSettings
            del self.ProjectName

        for i in range(len(self.ProjectStateChangerButtons)):
            destroy(self.ProjectStateChangerButtons[i].parent)
            destroy(self.ProjectStateChangerButtons[i])

        self.ProjectStateChangerButtons = []
        self.UniversalParentEntity.disable()
        self.CancelClick()

if __name__ == "__main__":
    from GamePlusEditor.OtherStuff import CurrentFolderNameReturner
    app = Ursina()
    pro = ConfigProjectManager(Entity(parent = camera.ui),f"{CurrentFolderNameReturner()}/Current Games",Func(print,"hi")).Show("mn")
    app.run()