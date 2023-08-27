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
from ursina.color import tint
from ProjectExporter import ProjectExporter
from ProjectEditor import ProjectEditor

class UrsinaEditor(Entity):
    def __init__(self,EditorCamera,**kwargs):
        super().__init__()
        self.WorldItems = [] #Every world items
        self.UDVars = [] #User defined vars
        self.UDFunc = [] #User defined functions
        self.UDSrc = [] #User defined script to run after making all the world items
        self.WindowConfing = [] #User defined script to run after making all the world items
        self.ToImport = {"from ursina import *","from panda3d.core import AntialiasAttrib"}

        # print("/...",list(self.ToImport))
        # self.WorldItemsModification = [] #Every change made to world items
        self.EditorCamera = EditorCamera
        self.NonConfiableEditorDataDefault = {"CurrentProjectNames": []}
        self.NonConfiableEditorData = OpenFile("Non configable editor data.txt",CurrentFolderNameReturner().replace("Editor","Editor data"),self.NonConfiableEditorDataDefault,True)
        self.InstructionList = []

        self.ConfiableEditorDataDefault = {"Show tooltip":True,"Coordinates": 0}
        self.ConfiableEditorDataDefaultType = [bool,int]
        self.ConfiableEditorData = OpenFile("Configable editor data.txt",CurrentFolderNameReturner().replace("Editor","Editor data"),self.ConfiableEditorDataDefault,True)
        self.FolderName = os.path.dirname(os.path.abspath(__file__))
        self.RecentEdits = ["",""]
        self.ProjectSettings = None

        self.MemoryCounter = MemoryCounter()
        self.StartingUi = StartingUI(EditorDataDict=  self.ConfiableEditorData,OnProjectStart=self.StartEdit,ExistingProjectsName=self.NonConfiableEditorData["CurrentProjectNames"],ChangeConfigDataToDefaultTypeFunc=self.ChangeConfigDataToDefaultType,ProjectName="",SaveNonConfiableData=self.SaveData,ShowInstructionFunc = self.ShowInstruction)
        # self.StartingUi.ShowRecentProjects()
        # self.StartingUi.RecentProjectsScrollerParentEntity.= len(self.StartingUi.TotalRunningProjects)

    def StartEdit(self):
        self.ProjectEditor = ProjectEditor(ExportToPyFunc=self.ExportProjectToPy,CurrentTabs=[],EditorCamera=EditorCamera,enabled = True)
        self.SceneEditor = SceneEditor(self.EditorCamera,enabled = True,WorldItems=self.WorldItems,SaveFunction= self.Save,ShowInstructionFunc = self.ShowInstruction,ToImport=self.ToImport,ExportToPyFunc=self.ExportProjectToPy,EditorCamera = EditorCamera)

        self.ProjectEditor.CurrnetTabs.append(self.SceneEditor)

        self.EditorCamera.item_to_in_find_on_mouse_hit_rotate = self.SceneEditor.WorldItems

        self.SceneEditor.enable()
        self.SceneEditor.UniversalParentEntity.enable()
        self.CheckAndStartSceneEditor(self.SceneEditor.UniversalParentEntity)
        # destroy(self.StartingUi,delay=2)
        # del self.StartingUi
        self.SceneEditor.GetPosTemp()
        self.SceneEditor.Setup()
        self.SetupSceneEditor()
        self.SceneEditor.DirectionEntity.enable()
        self.ProjectEditor.enable()
        self.ProjectEditor.UniversalParentEntity.enable()
        self.CheckAndStartSceneEditor(self.ProjectEditor.UniversalParentEntity)
        # self.Editor.Tempa.enable()
        # self.Editor.ignore = False

    def CheckAndStartSceneEditor(self,Entity):
        for i in range(len(Entity.children)):
            Entity.children[i].enable()
            if len(Entity.children[i].children) > 0:
                self.CheckAndStartSceneEditor(Entity.children[i])

    def SetupSceneEditor(self):
        self.SceneEditor.MakeEditorEnvironment(application.base.camNode,(255,255,255,0),(0.2399, .999, 0.1009, 0.938))

    def Save(self):
        self.WorldItems = self.SceneEditor.WorldItems
        self.ToImport = self.SceneEditor.ToImport
        # print(type(self.WorldItems[0]).__name__)
        self.ProjectSettings = self.StartingUi.ProjectSettings
        self.ProjectName = self.StartingUi.ProjectName
        # print(self.StartingUi.ProjectSettings)
        ProjectSaver(ProjectName = self.ProjectName,UdFunc = self.UDFunc,UdVar=self.UDVars,Udsrc=self.UDSrc,WindowConfig=self.WindowConfing,ToImport=list(self.ToImport),Items = self.WorldItems,Path=f'{FormatForSaving(self.FolderName)}Current Games',GameSettings=self.ProjectSettings)
        # print(type(self.ProjectName).__name__)
        if not self.ProjectName in self.NonConfiableEditorData["CurrentProjectNames"]:
            self.NonConfiableEditorData["CurrentProjectNames"].append(self.ProjectName)
            self.SaveData()

    def Setup(self):
        # self.EditorData = 
        self.StartingUi.Setup()
        self.StartingUi.ShowRecentProjects(self.WorldItems)

    def SaveData(self):
        # print("saveing")
        SaveFile("Non configable editor data.txt",CurrentFolderNameReturner().replace("Editor","Editor data"),self.NonConfiableEditorData)
        SaveFile("Configable editor data.txt",CurrentFolderNameReturner().replace("Editor","Editor data"),self.ConfiableEditorData)

    def ChangeConfigDataToDefaultType(self,Data: dict):
        try:
            for i in range(len(self.ConfiableEditorDataDefaultType)):
                if type(self.ConfiableEditorDataDefault[list(self.ConfiableEditorDataDefault)[i]]).__name__ == "int":
                    Data[list(Data)[i]] = int(Data[list(Data)[i]])

                elif type(self.ConfiableEditorDataDefault[list(self.ConfiableEditorDataDefault)[i]]).__name__ == "float":
                    Data[list(Data)[i]] = float(Data[list(Data)[i]])

                elif type(self.ConfiableEditorDataDefault[list(self.ConfiableEditorDataDefault)[i]]).__name__ == "bool":
                    if Data[list(Data)[i]].lower() == "true":
                        Data[list(Data)[i]] = True
                    elif Data[list(Data)[i]].lower() == "false":
                        Data[list(Data)[i]] = False

                elif type(self.ConfiableEditorDataDefault[list(self.ConfiableEditorDataDefault)[i]]).__name__ == "str":
                    Data[list(Data)[i]] = str(Data[list(Data)[i]])

                # self.ConfiableEditorDataDefaultType[i]

            self.ConfiableEditorData = Data
            # print("helo",self.ConfiableEditorData)
            self.StartingUi.EditorDataDict = self.ConfiableEditorData
            self.StartingUi.ConfigEditorAsSettings()

        except Exception as e:
            print(e)

    def ShowInstruction(self,Str,Color = tint(color.white,-.6)):
        self.InstructionList.append(InstructionMenu(ToSay=Str,OnXClick=Func(self.DestroyInstruction,Index = -1),DestroyFunc=Func(self.DestroyInstruction,Index = -1),Color=Color))


    def DestroyInstruction(self,Index):
        # print("helo")
        for i in range(len(self.InstructionList)):
            destroy(self.InstructionList[i])



    def ExportProjectToPy(self):
        self.ToSaveWorldItems = self.SceneEditor.WorldItems
        self.ToSaveToImport = self.SceneEditor.ToImport
        self.ToSaveProjectSettings = self.StartingUi.ProjectSettings
        self.ToSaveProjectName = self.StartingUi.ProjectName
        ProjectExporter(ProjectName = self.ToSaveProjectName,ProjectPath=f'{FormatForSaving(self.FolderName)}Current Games',ToSavePath=f'{FormatForSaving(self.FolderName)}Exported games')



if __name__ == "__main__":
    from panda3d.core import AntialiasAttrib
    app = Ursina(editor_ui_enabled = True)
    window.fps_counter.disable()
    window.exit_button.disable()
    Sky()
    DataToLoad = {"Show tooltip":True,"Coordinates": 0}
    Editor = UrsinaEditor(EditCam := EditorCamera(),DataToLoad = DataToLoad) # the ':=' operator is called walrus operator. google it!  
    Editor.Setup()
    render.setAntialias(AntialiasAttrib.MAuto)

    # EditCam.item_to_in_find_on_mouse_hit_rotate = Editor.SceneEditor.WorldItems
    app.run()