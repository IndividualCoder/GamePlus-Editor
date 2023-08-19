from ursina import *
from StartingUI import StartingUI
from SceneEditor  import SceneEditor
from ProjectSaver import ProjectSaver
# from CurrentFolderNameReturner import CurrentFolderNameReturner
from OtherStuff import FormatForSaving,CurrentFolderNameReturner
import os
from OpenFile import OpenFile

class UrsinaEditor(Entity):
    def __init__(self,EditorCamera,DataToLoad):
        super().__init__()
        self.WorldItems = [] #Every world items
        self.UDVars = [] #User defined vars
        self.UDFunc = [] #User defined functions
        self.UDSrc = [] #User defined script to run after making all the world items
        self.WindowConfing = [] #User defined script to run after making all the world items
        # self.WorldItemsModification = [] #Every change made to world items
        self.CurrentProjectNames = []
        self.EditorCamera = EditorCamera
        self.EditorData = OpenFile("Editor data.txt",CurrentFolderNameReturner().replace("Editor","Editor data"),DataToLoad,True)
        self.FolderName = os.path.dirname(os.path.abspath(__file__))
        self.RecentEdits = ["",""]
        self.ProjectSettings = None


        self.StartingUi = StartingUI(NameOfChangeVarsList=list(self.EditorData),TypeOfChangeVarsList = [sublist[1] for sublist in self.EditorData.values()],DefaultValueOfChangeVarsList = [sublist[0] for sublist in self.EditorData.values()],OnProjectStart=self.StartEdit,ExistingProjectsName=self.CurrentProjectNames,ProjectName="")
        self.Editor = SceneEditor(self.EditorCamera,enabled = False,WorldItems=self.WorldItems,SaveFunction= self.Save)

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

    def Setup(self):
        # self.EditorData = 
        self.StartingUi.Setup()
        self.StartingUi.ShowRecentProjects(self.WorldItems)

    # def update(self):
    #     print(self.WorldItems)

if __name__ == "__main__":
    from ursina.prefabs.memory_counter import MemoryCounter
    MemoryCounter()
    
    app = Ursina(editor_ui_enabled = True)
    window.fps_counter.disable()
    window.exit_button.disable()
    Sky()
    Editor = UrsinaEditor(EditCam := EditorCamera(),DataToLoad = {"Show tooltip":[True,"bool"],"Coordinates": [0,"int"]}) # the ':=' operator is called walrus operator. google it!  
    Editor.Setup()
    EditCam.item_to_in_find_on_mouse_hit_rotate = Editor.Editor.WorldItems
    app.run()