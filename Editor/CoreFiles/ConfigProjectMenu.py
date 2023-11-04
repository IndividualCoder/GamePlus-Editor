import sys
import os

# Make the main to 'Editor' so we can access the files of the 'Editor' folder
editor_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
sys.path.append(editor_directory)

from ursina import *
import json
from OtherStuff import CurrentFolderNameReturner
from CoreFiles.TrueFalseIndicator import TrueFalseIndicator

class ConfigProjectManager(Entity):
    '''Not done yet ;)'''
    def __init__(self,Parent,Path,CancelClick,ToSaveDataFunc = Func(print,"hi")):
        super().__init__(parent = Parent)
        self.ProjectPath = Path
        self.CancelClick = CancelClick
        self.ConfigProjectStateList = [["Low","Medium","High"],["Python","Ursa-visor"],["True","False"],["windows","mac","ios","Linux","android"],["FPC","TPC","TopDown","Platformer","FPCTPC"]]
        self.ToSaveDataFunc = ToSaveDataFunc
        self.CurrentProjectName: str = None

        self.ProjectStateChangerButtons = []

        self.UniversalParentEntity = Entity(parent = self,enabled = False)
        self.BackGround = Entity(parent = self.UniversalParentEntity,model = "cube",scale = 10,color = color.black66)
        
        self.CancelButton = Button(parent = self.UniversalParentEntity,name = "cancel button",text = "Cancel",position = Vec3(-0.74, 0.42, 0) , rotation = Vec3(0, 0, 0) , scale = Vec3(0.270001, 0.13, 1),on_click = self.Close)
        self.SaveButton = Button(parent = self.UniversalParentEntity,name = "save buton",text = "Save and exit",position = Vec3(-0.46, 0.42, 0) , rotation = Vec3(0, 0, 0) , scale = Vec3(0.270001, 0.130001, 1),on_click = self.ConfigProjectAsSettings)


    def Show(self,Name):
        with open(f"{self.ProjectPath}/{Name}/Game settings.txt","r")  as File:
            self.GameSettings = json.load(File)
            self.ProjectName = Name
        for i,j in enumerate(self.GameSettings):
            self.a = Text(f"{j}:",parent = self.UniversalParentEntity,y = .32-i*.1,x = -.5,scale = 2,z = -1)
            self.ProjectStateChangerButtons.append(TrueFalseIndicator(parent = self.a,DefaultState=str(self.GameSettings[j]),StateList= self.ConfigProjectStateList[i],position = (.5,0,0),scale = (.2,.025,1)))
        self.a = Text(f"Name: ",parent = self.UniversalParentEntity,y = .32-5*.1,x = -.5,scale = 2,z = -1,enabled = False)
        self.ProjectStateChangerButtons.append(InputField(parent = self.a,default_value=Name,position = (.5,0,0),scale = (.2,.025,1),active = False,enabled = False))

    def ConfigProjectAsSettings(self):
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
                    os.rename(f"{CurrentFolderNameReturner().replace('Editor','Current Games')}/{self.ProjectName}",f"{CurrentFolderNameReturner().replace('Editor','Current Games')}/{self.ProjectStateChangerButtons[-1].text}")
                    self.ProjectName  = self.ProjectStateChangerButtons[-1].text

                with open(f'{self.ProjectPath}/{self.ProjectName}/Game settings.txt',"w") as File:
                    json.dump(self.GameSettings,File)
                print(self.CurrentProjectName)
                self.ToSaveDataFunc(Name = self.CurrentProjectName,Replace = self.ProjectName)

                self.Close()

    def Close(self):
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
    from OtherStuff import CurrentFolderNameReturner
    app = Ursina()
    pro = ConfigProjectManager(Entity(parent = camera.ui),CurrentFolderNameReturner().replace("Editor","Current games"),Func(print,"hi")).Show("mn")
    app.run()