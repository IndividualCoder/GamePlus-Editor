from ursina import *
from StartingUI import StartingUI
from SceneEditor  import SceneEditor
from ProjectSaver import ProjectSaver
# from CurrentFolderNameReturner import CurrentFolderNameReturner
from OtherStuff import FormatForSaving,CurrentFolderNameReturner
import os
from OpenFile import OpenFile,SaveFile,OpenSeletor
from ursina.prefabs.memory_counter import MemoryCounter
from CoreFiles.InstructionMenu import InstructionMenu
from ursina.color import tint
from ProjectExporter import ProjectExporter
from ProjectEditor import ProjectEditor
from CodeEditorPython import CodeEditorPython



class UrsinaEditor(Entity):
    def __init__(self,EditorCamera,**kwargs):
        super().__init__()
        self.WorldItems = [] #Every world items
        self.UDVars = [] #User defined vars
        self.UDFunc = [] #User defined functions
        self.UDSrc = [] #User defined script to run after making all the world items
        self.WindowConfing = [] #User defined script to run after making all the world items
        self.ToImport = {"from ursina import *","from panda3d.core import AntialiasAttrib"}
        self.CurrentSupportedEditors = ["Scene editor","Code editor","Ursa-vison editor"]
        self.AddCurrentSupportedEditors = [self.AddSceneEditor,self.AddCodeEditor,self.AddUrsaVisorEditor]
        self.CurrentEditor = None

        self.EditorCamera = EditorCamera
        self.NonConfiableEditorDataDefault = {"CurrentProjectNames": []}
        self.NonConfiableEditorData = OpenFile("Non configable editor data.txt",CurrentFolderNameReturner().replace("Editor","Editor data"),self.NonConfiableEditorDataDefault,True)
        self.InstructionList = []

        self.ConfiableEditorDataDefault = {"Show tooltip":True,"Test": 0}
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
        self.ProjectEditor = ProjectEditor(ExportToPyFunc=self.ExportProjectToPy,CurrentTabs=[],EditorCamera=self.EditorCamera,enabled = True)
        self.ProjectEditor.SetUp()
        self.AddSceneEditor()
        self.SceneEditor = self.ProjectEditor.CurrentTabs[-1]
        # self.ProjectEditor.UpdateTabsMenu()
        self.EditorCamera.item_to_in_find_on_mouse_hit_rotate = self.CurrentEditor.WorldItems

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

    def SetupEditor(self,Editor:str):
        if Editor.name.startswith("Scene"):
            Editor.MakeEditorEnvironment(application.base.camNode,(255,255,255,0),(0.2399, .999, 0.1009, 0.938))

    def Save(self):
        # self.WorldItems = self.SceneEditor.WorldItems
        # self.ToImport = self.SceneEditor.ToImport
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
        try:
            self.ProjectEditor.UpdateTabsMenu()
        except:
            pass
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

    def AddSceneEditor(self):
        self.ProjectEditor.CurrentTabs.append(SceneEditor(enabled = True,WorldItems=self.WorldItems,SaveFunction= self.Save,ShowInstructionFunc = self.ShowInstruction,ToImport=self.ToImport,ExportToPyFunc=self.ExportProjectToPy,EditorCamera = self.EditorCamera))

        self.ProjectEditor.CurrentTabs[-1].name = f"Scene Editor {len([i for i in range(len(self.ProjectEditor.CurrentTabs)) if type(self.ProjectEditor.CurrentTabs).__name__ == 'SceneEditor'])}"

        self.ProjectEditor.UpdateTabsMenu()

        self.CurrentEditor = self.ProjectEditor.CurrentTabs[-1]

        self.CurrentEditor.enable()
        self.CurrentEditor.UniversalParentEntity.enable()
        self.CheckAndStartSceneEditor(self.CurrentEditor.UniversalParentEntity)
        # destroy(self.StartingUi,delay=2)
        # del self.StartingUi

        self.CurrentEditor.GetPosTemp()
        self.CurrentEditor.Setup()
        self.SetupEditor(self.CurrentEditor)
        self.CurrentEditor.DirectionEntity.enable()

    def AddCodeEditor(self):
        self.ProjectEditor.CurrentTabs.append(CodeEditorPython(enabled=False))

        self.ProjectEditor.CurrentTabs[-1].name = f"Code Editor {len([i for i in range(len(self.ProjectEditor.CurrentTabs)) if type(self.ProjectEditor.CurrentTabs).__name__ == 'CodeEditorPython'])}" 

        self.ProjectEditor.UpdateTabsMenu()

    def AddUrsaVisorEditor(self):
        self.ProjectEditor.CurrentTabs.append(CodeEditorPython(enabled=False))

        self.ProjectEditor.CurrentTabs[-1].name = f"Ursa Editor {len([i for i in range(len(self.ProjectEditor.CurrentTabs)) if type(self.ProjectEditor.CurrentTabs).__name__ == 'CodeEditorPython'])}" 

        self.ProjectEditor.UpdateTabsMenu()

    def DestroyInstruction(self,Index = None):
        # print("helo")
        for i in range(len(self.InstructionList)):
            # self.InstructionList[i].kill(.2)
            destroy(self.InstructionList[i],delay=.3)



    def ExportProjectToPy(self,Path):
        self.Save()
        self.ToSaveWorldItems = self.SceneEditor.WorldItems
        self.ToSaveToImport = self.SceneEditor.ToImport
        self.ToSaveProjectSettings = self.StartingUi.ProjectSettings
        self.ToSaveProjectName = self.StartingUi.ProjectName
        Path.replace("\\","/")
        Path += "/Exported games"
        print(Path)

        ProjectExporter(ProjectName = self.ToSaveProjectName,ProjectPath=f'{FormatForSaving(self.FolderName)}Current Games',ToSavePath=Path)
        # print(Path.split("/",-1))
        self.ShowInstruction("Exported successfully")
    # def input(self,key):
    #     print(key)


if __name__ == "__main__":
    from panda3d.core import AntialiasAttrib
    from direct.filter.CommonFilters import CommonFilters
    app = Ursina()
    window.exit_button.disable()
    window.fps_counter.disable()
    # window.fullscreen = True
    Sky()

    # filters = CommonFilters(base.win, base.cam)

    # filters.setCartoonInk(separation  = .9)

    # from ursina.shaders.basic_lighting_shader import basic_lighting_shader
    # camera.shader = basic_lighting_shader
    # from ursina.camera
    # def input(key):
    #     if key == "-":
    #         Editor.ProjectEditor.UpdateTabsMenu()

    Editor = UrsinaEditor(EditCam := EditorCamera()) # the ':=' operator is called walrus operator. google it!  
    Editor.Setup()
    render.setAntialias(AntialiasAttrib.MAuto)
    app.run()