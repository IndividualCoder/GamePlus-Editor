from ursina import *
from StartingUI import StartingUI
from SceneEditor  import SceneEditor
from ProjectSaver import ProjectSaver
# from CurrentFolderNameReturner import CurrentFolderNameReturner
from OtherStuff import FormatForSaving,CurrentFolderNameReturner
import os
from OpenFile import OpenFile,SaveFile
from ursina.prefabs.memory_counter import MemoryCounter
from CoreFiles.InstructionMenu import InstructionMenu

class UrsinaEditor(Entity):
    def __init__(self,EditorCamera,DataToLoad):
        super().__init__()
        self.WorldItems = [] #Every world items
        self.UDVars = [] #User defined vars
        self.UDFunc = [] #User defined functions
        self.UDSrc = [] #User defined script to run after making all the world items
        self.WindowConfing = [] #User defined script to run after making all the world items
        # self.WorldItemsModification = [] #Every change made to world items
        self.EditorCamera = EditorCamera
        self.NonConfiableEditorDataDefault = {"CurrentProjectNames": []}
        self.NonConfiableEditorData = OpenFile("Non configable editor data.txt",CurrentFolderNameReturner().replace("Editor","Editor data"),self.NonConfiableEditorDataDefault,True)
        self.InstructionList = []

        self.ConfiableEditorData = OpenFile("Configable editor data.txt",CurrentFolderNameReturner().replace("Editor","Editor data"),DataToLoad,True)
        self.FolderName = os.path.dirname(os.path.abspath(__file__))
        self.RecentEdits = ["",""]
        self.ProjectSettings = None

        self.MemoryCounter = MemoryCounter()
        self.StartingUi = StartingUI(EditorDataDict=  self.ConfiableEditorData,OnProjectStart=self.StartEdit,ExistingProjectsName=self.NonConfiableEditorData["CurrentProjectNames"],ProjectName="",SaveNonConfiableData=self.SaveData,ShowInstructionFunc = self.ShowInstruction)
        self.Editor = SceneEditor(self.EditorCamera,enabled = False,WorldItems=self.WorldItems,SaveFunction= self.Save,ShowInstructionFunc = self.ShowInstruction)

        # self.StartingUi.ShowRecentProjects()
        # self.StartingUi.RecentProjectsScrollerParentEntity.= len(self.StartingUi.TotalRunningProjects)

    def StartEdit(self):
        self.Editor.enable()
        self.Editor.UniversalParentEntity.enable()
        self.CheckAndStartSceneEditor(self.Editor.UniversalParentEntity)
        # destroy(self.StartingUi,delay=2)
        # del self.StartingUi
        self.Editor.GetPosTemp()
        self.SetupSceneEditor()
        self.Editor.DirectionEntity.enable()
        # self.Editor.Tempa.enable()
        # self.Editor.ignore = False

    def CheckAndStartSceneEditor(self,Entity):
        for i in range(len(Entity.children)):
            Entity.children[i].enable()
            if len(Entity.children[i].children) > 0:
                self.CheckAndStartSceneEditor(Entity.children[i])

    def SetupSceneEditor(self):
        self.Editor.MakeEditorEnvironment(application.base.camNode,(255,255,255,0),(0.2399, .999, 0.1009, 0.938))

    def Save(self):
        self.WorldItems = self.Editor.WorldItems
        # print(type(self.WorldItems[0]).__name__)
        self.ProjectSettings = self.StartingUi.ProjectSettings
        self.ProjectName = self.StartingUi.ProjectName
        # print(self.StartingUi.ProjectSettings)
        ProjectSaver(ProjectName = self.ProjectName,UdFunc = self.UDFunc,UdVar=self.UDVars,Udsrc=self.UDSrc,WindowConfig=self.WindowConfing,Items = self.WorldItems,Path=f'{FormatForSaving(self.FolderName)}Current Games',GameSettings=self.ProjectSettings)
        # print(type(self.ProjectName).__name__)
        if not self.ProjectName in self.NonConfiableEditorData["CurrentProjectNames"]:
            self.NonConfiableEditorData["CurrentProjectNames"].append(self.ProjectName)
            self.SaveData()

    def Setup(self):
        # self.EditorData = 
        self.StartingUi.Setup()
        self.StartingUi.ShowRecentProjects(self.WorldItems)

    def SaveData(self):
        SaveFile("Non configable editor data.txt",CurrentFolderNameReturner().replace("Editor","Editor data"),self.NonConfiableEditorData)
        SaveFile("Configable editor data.txt",CurrentFolderNameReturner().replace("Editor","Editor data"),self.ConfiableEditorData)

    def ShowInstruction(self,Str):
        self.InstructionList.append(InstructionMenu(ToSay=Str,OnXClick=Func(print,"-1"),DestroyFunc=Func(self.DestroyInstruction,-1)))

    def DestroyInstruction(self,Index):
        print("helo")
        for i in range(len(self.InstructionList)):
            destroy(self.InstructionList[i])

    # def update(self):
    #     print(self.WorldItems)

if __name__ == "__main__":
    
    app = Ursina(editor_ui_enabled = True)
    window.fps_counter.disable()
    window.exit_button.disable()
    Sky()
    DataToLoad = {"Show tooltip":True,"Coordinates": 0}
    Editor = UrsinaEditor(EditCam := EditorCamera(),DataToLoad = DataToLoad) # the ':=' operator is called walrus operator. google it!  
    Editor.Setup()
    EditCam.item_to_in_find_on_mouse_hit_rotate = Editor.Editor.WorldItems
    app.run()