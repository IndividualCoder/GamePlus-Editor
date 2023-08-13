from ursina import *
from StartingUI import StartingUI
from SceneEditor  import SceneEditor
from ProjectSaver import ProjectSaver
from CurrentFolderNameReturner import CurrentFolderNameReturner
from OtherStuff import FormatForSaving
import os

class UrsinaEditor(Entity):
    def __init__(self,EditorCamera):
        super().__init__()
        self.WorldItems = [] #Every world items
        self.UDVars = [] #User defined vars
        self.UDFunc = [] #User defined functions
        self.UDSrc = [] #User defined script to run after making all the world items
        self.WindowConfing = [] #User defined script to run after making all the world items
        # self.WorldItemsModification = [] #Every change made to world items
        self.CurrentProjectNames = []
        self.EditorCamera = EditorCamera
        self.NameOfChangeVarList = ["Test var"]
        self.TypeOfChangeVarList = ["Unknown"]
        self.DefaultValueOfChageVarList = ["None"]
        self.FolderName = os.path.dirname(os.path.abspath(__file__))
        self.RecentEdits = ["",""]
        self.ProjectSettings = None

        self.StartingUi = StartingUI(NameOfChangeVarsList=self.NameOfChangeVarList,TypeOfChangeVarsList = self.TypeOfChangeVarList,DefaultValueOfChangeVarsList = self.DefaultValueOfChageVarList,OnProjectStart=self.StartEdit,ExistingProjectsName=self.CurrentProjectNames,ProjectName="")
        self.Editor = SceneEditor(self.EditorCamera,enabled = False,WorldItems=self.WorldItems,SaveFunction= self.Save)

        self.StartingUi.ShowRecentProjects()
        # self.StartingUi.RecentProjectsScrollerParentEntity.= len(self.StartingUi.TotalRunningProjects)
    def StartEdit(self):
        self.Editor.enable()
        self.Editor.UniversalParentEntity.enable()
        self.CheckAndStartSceneEditor(self.Editor.UniversalParentEntity)
        # destroy(self.StartingUi,delay=2)
        # del self.StartingUi
        self.Editor.GetPosTemp()
        self.SetupEditor()
        self.Editor.DirectionEntity.enable()
        # self.Editor.ignore = False

    def CheckAndStartSceneEditor(self,Entity):
        for i in range(len(Entity.children)):
            Entity.children[i].enable()
            if len(Entity.children[i].children) > 0:
                self.CheckAndStartSceneEditor(Entity.children[i])

    def SetupEditor(self):
        self.Editor.MakeEditorEnvironment(application.base.camNode,(255,255,255,0),(0.2399, .999, 0.1009, 0.938))

    def Save(self):
        self.WorldItems = self.Editor.WorldItems
        self.ProjectSettings = self.StartingUi.ProjectSettings
        self.ProjectName = self.StartingUi.ProjectName
        # print(self.StartingUi.ProjectSettings)
        ProjectSaver(ProjectName = self.ProjectName,UdFunc = self.UDFunc,UdVar=self.UDVars,Udsrc=self.UDSrc,WindowConfig=self.WindowConfing,Items = self.WorldItems,Path=f'{FormatForSaving(self.FolderName)}Current Games',GameSettings=self.ProjectSettings)

if __name__ == "__main__":
    from ursina.prefabs.memory_counter import MemoryCounter
    MemoryCounter()
    app = Ursina(editor_ui_enabled = True)
    window.fps_counter.disable()
    window.exit_button.disable()
    Sky()
    UrsinaEditor(EditorCamera())
    app.run()